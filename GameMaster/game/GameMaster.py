from __future__ import annotations
import asyncio
import sys
import traceback
from typing import List

from game.FinishedReason import FinishedReason
from game.GameContxt import GameContext
from game.GameFinishedException import GameFinishedException
from WebsocketServer import WebsocketServer
from game.SecretNumber import SecretNumber
from game.action.ActionFactory import ActionFactory
from game.action.ActionType import ActionType
from game.action.BaseAction import BaseAction
from game.action.Challenge import Challenge
from game.actionResult.BaseActionResult import BaseActionResult
from game.actionResult.ChallengeResult import ChallengeResult
from player.Player import Player
from player.PlayerFactory import PlayerFactory
from player.PlayerNumber import PlayerNumber
from viewer.Viewer import Viewer

TIMEOUT_SEC = 10
GAME_WAIT = 0
DEBUG = False


class Master:
    def __init__(self, server: WebsocketServer, p1: Player, p2: Player, viewer: Viewer, loop: asyncio.AbstractEventLoop):
        self.__server = server
        self.__loop = loop
        self.__p1 = p1
        self.__p2 = p2
        self.__viewer = viewer
        self.__context = GameContext(p1, p2)
        self.__action_log: List[BaseAction] = []
        self.__action_result_log: List[BaseActionResult] = []

    @property
    def context(self) -> GameContext:
        return self.__context

    @staticmethod
    async def create_game(server: WebsocketServer, viewer: Viewer, loop: asyncio.AbstractEventLoop) -> Master:
        print(f"waiting connection at {server.server_url()}")
        p1 = await PlayerFactory.create(server, PlayerNumber.Player1, loop)
        p2 = await PlayerFactory.create(server, PlayerNumber.Player2, loop)
        return Master(server, p1, p2, viewer, loop)

    async def start_match(self):
        try:
            await self.initialize_players()
            await self.__viewer.send_players(self.context)
            self.ensure_player_name()

        except GameFinishedException as e:
            if e.winner is not None:
                self.context.add_score(e.winner.player_number)
        else:
            for round_number in range(1, 5):
                print(f'start round {round_number}')
                round_winner = await self.start_game()

                await self.send_round_result(round_winner)
                self.context.add_score(round_winner)

                # await asyncio.sleep(5)
                await self.next_round()

        winner = self.context.get_winner()
        self.context.print_result()
        await self.send_game_result(winner)

    async def next_round(self):
        self.context.switch_start_player()
        self.context.reset_turn()
        self.context.clear_used_item()
        self.context.clear_ap()
        self.context.round += 1

    async def start_game(self) -> PlayerNumber:
        prev_actions: List[BaseActionResult] = []
        try:
            await self.initialize_secrets()
            await self.__viewer.send_secret_numbers(self.context)

            while True:
                current_player = self.context.get_current_player()

                print(f'turn {self.context.turn_count}.')
                print(f'player {current_player.player_number} action')

                prev_actions = await self.turn_action(current_player, prev_actions)
                self.context.next_turn()

        except GameFinishedException as e:
            winner = e.winner
            self.print_finish_reason(e.reason, e.detail)
        except Exception as e:
            winner = self.context.get_opponent_player()
            if DEBUG:
                etype, value, tb = sys.exc_info()
                for line in traceback.format_exception(etype, value, tb):
                    print(line)

        return winner.player_number

    async def turn_action(self, player: Player, prev_actions: List[BaseActionResult]) -> List[BaseActionResult]:
        action_results: List[BaseActionResult] = []
        player_number = player.player_number

        try:
            await player.send_opponent_action_results(prev_actions)
            prev_action_result = await self.item_action(player)
            if prev_action_result is not None:
                print(f"use: {prev_action_result.action.actionType}")
                action_results.append(prev_action_result)
                self.context.set_used_item(player_number, prev_action_result.action.actionType)
                self.context.add_ap(player_number, prev_action_result.action.actionType)
                await asyncio.sleep(GAME_WAIT)

            challenge_result = await self.challenge_action(player)
            print(f"challenge: {challenge_result.action.number}")
            action_results.append(challenge_result)
            self.context.add_ap(player_number, challenge_result.action.actionType)
            if challenge_result.matched:
                raise GameFinishedException(player, FinishedReason.all_hit)
            await asyncio.sleep(GAME_WAIT)

            post_action_result = await self.item_action(player)
            if post_action_result is not None:
                print(f"use: {post_action_result.action.actionType}")
                action_results.append(post_action_result)
                self.context.set_used_item(player_number, post_action_result.action.actionType)
                self.context.add_ap(player_number, post_action_result.action.actionType)
                if prev_action_result is not None:
                    raise GameFinishedException(self.context.get_opponent_player(), FinishedReason.invalid_action,
                                                "use 2 items in a turn.")
                if post_action_result.action.actionType in [ActionType.Target, ActionType.HighLow]:
                    raise GameFinishedException(self.context.get_opponent_player(), FinishedReason.invalid_action,
                                                "use attack item after challenge.")
                await asyncio.sleep(GAME_WAIT)

            return action_results
        except GameFinishedException:
            raise
        except Exception as e:
            if DEBUG:
                etype, value, tb = sys.exc_info()
                for line in traceback.format_exception(etype, value, tb):
                    print(line)
            raise GameFinishedException(self.context.get_opponent_player(), FinishedReason.invalid_action, str(e.args))

    async def challenge_action(self, player: Player) -> ChallengeResult:
        try:
            challenge_number = await asyncio.wait_for(player.request_challenge_number(), TIMEOUT_SEC)
        except asyncio.TimeoutError:
            raise GameFinishedException(self.context.get_opponent_player(), FinishedReason.timeout)
        action: Challenge = ActionFactory.create_action(ActionType.Challenge, challenge_number, player)
        await self.add_action_log(action)
        action_result = action.process_action(self.__context)
        await self.add_action_result_log(action_result)
        await player.send_action_result(action_result)
        return action_result

    async def item_action(self, player: Player) -> BaseActionResult | None:
        try:
            action_type, number = await asyncio.wait_for(player.request_item_action(), TIMEOUT_SEC)
        except asyncio.TimeoutError:
            raise GameFinishedException(self.context.get_opponent_player(), FinishedReason.timeout)
        action = ActionFactory.create_action(action_type, number, player)
        await self.add_action_log(action)
        action_result = action.process_action(context=self.__context)
        await self.add_action_result_log(action_result)
        await player.send_action_result(action_result)
        return action_result if action_result.action.actionType != ActionType.Pass else None

    async def initialize_players(self):
        for player in self.context.get_players():
            try:
                await player.send_player_number()
                await self.initialise_player_name(player)
            except Exception:
                if DEBUG:
                    etype, value, tb = sys.exc_info()
                    for line in traceback.format_exception(etype, value, tb):
                        print(line)

    async def initialise_player_name(self, player: Player):
        name = await player.request_player_name()
        player.player_name = name

    def ensure_player_name(self):
        initialized = [PlayerNumber.Player1, PlayerNumber.Player2]
        for player in self.context.get_players():
            if player.player_name is None:
                initialized.remove(player.player_number)

        if len(initialized) != 2:
            player_number = initialized[0] if len(initialized) > 0 else None
            raise GameFinishedException(
                self.context.get_player(player_number) if player_number is not None else None,
                FinishedReason.initialize_error
            )

    async def initialize_secrets(self):
        self.context.reset_secrets()
        await self.initialise_secret(PlayerNumber.Player1)
        await self.initialise_secret(PlayerNumber.Player2)

    async def initialise_secret(self, player_number: PlayerNumber):
        player = self.context.get_player(player_number)
        try:
            secret_str = await player.request_secret_number()
            secret = SecretNumber(number=secret_str)
            self.context.set_secret_number(player_number, secret)
        except Exception:
            etype, value, tb = sys.exc_info()
            print(traceback.format_exception(etype, value, tb))
            opponent_player = PlayerNumber.Player2 if player_number == PlayerNumber.Player1 else PlayerNumber.Player1
            raise GameFinishedException(self.context.get_player(opponent_player), FinishedReason.invalid_secret)


    async def send_round_result(self, winner: PlayerNumber):
        for player in self.context.get_players():
            await player.send_round_result(winner)
        await self.__viewer.send_round_result(winner, self.context)
        print(f"round winner player{winner.value}")

    async def send_game_result(self, winner: PlayerNumber | None):
        for player in self.context.get_players():
            await player.send_game_result(winner)
        await self.__viewer.send_game_result(winner, self.context)
        if winner is not None:
            print(f"game winner player{winner.value}")
        else:
            print("draw")

    async def add_action_log(self, action: BaseAction):
        if DEBUG:
            if action.actionType in [ActionType.Challenge, ActionType.Target, ActionType.Shuffle, ActionType.Change]:
                number = f' number: {action.number}'
            else:
                number = ''
            print(f"action: {action.actionType}{number}")
        self.__action_log.append(action)

    async def clear_action_log(self):
        self.__action_log.clear()

    async def dump_action_log(self):
        pass

    async def add_action_result_log(self, action_result: BaseActionResult):
        if DEBUG:
            from game.actionResult.HighLowResult import HighLowResult
            from game.actionResult.TargetRsult import TargetResult
            if isinstance(action_result, ChallengeResult):
                detail = f" detail: hit {action_result.hit} blow {action_result.blow}"
            elif isinstance(action_result, HighLowResult):
                detail = f" detail: high {action_result.high} low {action_result.low}"
            elif isinstance(action_result, TargetResult):
                detail = f" detail: position {action_result.position}"
            else:
                detail = ""
            print(f"action result: {action_result.action.actionType}{detail}")
        self.__action_result_log.append(action_result)
        await self.__viewer.send_action_result(action_result, self.context)

    async def clear_action_result_log(self):
        self.__action_result_log.clear()

    async def dump_action_result_log(self):
        pass

    def print_finish_reason(self, reason: FinishedReason, detail: str):
        reason_str: str = ""
        if reason == FinishedReason.all_hit:
            reason_str = "hit all digits"
        if reason == FinishedReason.invalid_action:
            reason_str = "invalid action"
        if reason == FinishedReason.timeout:
            reason_str = "player action timeout"

        print(f"{reason_str} : {detail}")
