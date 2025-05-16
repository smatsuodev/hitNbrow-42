from typing import List

from game.APStore import APStore
from game.RoundResults import RoundResults
from game.Score import Score
from game.SecretNumber import SecretNumber
from game.Turn import Turn
from game.UsedActions import UsedActions
from game.action.ActionType import ActionType
from player.Player import Player
from player.PlayerNumber import PlayerNumber


class GameContext:

    def __init__(self, p1: Player, p2: Player):
        self.p1 = p1
        self.p2 = p2
        self.p1_secret = None
        self.p2_secret = None
        self.p1_action_point = 0
        self.p2_action_point = 0
        self.p1_used_item = UsedActions()
        self.p2_used_item = UsedActions()
        self.p1_ap_store = APStore()
        self.p2_ap_store = APStore()
        self.start_player = Turn.Player1
        self.current_turn = Turn.Player1
        self.turn_count = 1
        self.round = 1
        self.roundResults = RoundResults()

    def get_player(self, player_number: PlayerNumber) -> Player:
        return self.p1 if player_number == PlayerNumber.Player1 else self.p2

    def get_players(self) -> List[Player]:
        return [self.p1, self.p2]

    def next_turn(self):
        self.turn_count += 1
        self.current_turn = Turn.Player1 if self.current_turn == Turn.Player2 else Turn.Player2

    def get_current_player(self) -> Player:
        return self.p1 if self.current_turn == Turn.Player1 else self.p2

    def get_opponent_player(self) -> Player:
        return self.p1 if self.current_turn == Turn.Player2 else self.p2

    def set_secret_number(self, player_number: PlayerNumber, secret: SecretNumber):
        if player_number == PlayerNumber.Player1:
            self.p1_secret = secret
        else:
            self.p2_secret = secret

    def get_secret_number(self, player_number: PlayerNumber) -> SecretNumber:
        return self.p1_secret if player_number == PlayerNumber.Player1 else self.p2_secret

    def get_opponent_secret_number(self, player_number: PlayerNumber) -> SecretNumber:
        return self.p2_secret if player_number == PlayerNumber.Player1 else self.p1_secret

    def get_used_item(self, player_number: PlayerNumber):
        return self.p1_used_item if player_number == PlayerNumber.Player1 else self.p2_used_item

    def set_used_item(self, player_number: PlayerNumber, action: ActionType):
        used_item = self.p1_used_item if player_number == PlayerNumber.Player1 else self.p2_used_item
        used_item.append(action)

    def clear_used_item(self):
        self.p1_used_item.clear()
        self.p2_used_item.clear()

    def get_ap_store(self, player_number: PlayerNumber) -> APStore:
        return self.p1_ap_store if player_number == PlayerNumber.Player1 else self.p2_ap_store

    def add_ap(self, player_number: PlayerNumber, action: ActionType):
        store = self.p1_ap_store if player_number == PlayerNumber.Player1 else self.p2_ap_store
        store.did_action(action)

    def clear_ap(self):
        self.p1_ap_store.clear()
        self.p2_ap_store.clear()

    def reset_turn(self):
        self.current_turn = self.start_player
        self.turn_count = 1

    def switch_start_player(self):
        self.start_player = Turn.Player1 if self.start_player == Turn.Player2 else Turn.Player2

    def reset_secrets(self):
        self.p1_secret = None
        self.p2_secret = None

    def add_action_point(self, player_number: PlayerNumber, increase: int):
        if player_number == PlayerNumber.Player1:
            self.p1_action_point += increase
        else:
            self.p2_action_point += increase

    def ensure_secret(self):
        if self.p1_secret is None or self.p2_secret is None:
            raise ValueError("secrets is not initialized.")

    def add_score(self, winner: PlayerNumber):
        self.roundResults.append_result(winner, self.p1_ap_store.current_ap, self.p2_ap_store.current_ap)

    def get_winner(self) -> PlayerNumber | None:
        return self.roundResults.get_winner()

    def print_result(self):
        self.roundResults.print_results(self.p1.player_name, self.p2.player_name)
