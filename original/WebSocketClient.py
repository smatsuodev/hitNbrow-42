import argparse
import asyncio
import sys
from typing import Literal
import websockets
import json



from player.sendMessage.ChallengeNumberResponse import ChallengeNumberResponse
from player.sendMessage.PlayerNameResponse import PlayerNameResponse
from player.sendMessage.SecretNumberResponse import SecretNumberResponse
from util.util import add_change, add_shuffle, delete_bad_answer, delete_bad_answer_high_low, delete_bad_answer_target, create_unique_list
from strategy import secret
from strategy import estimate
from strategy import candidate
from strategy import item

DOMAIN = 'localhost'
PORT = 8088
NAME = 'JO'
DENGERTHRESHOLD = 500
WARNINGTHRESHOLD = 1000

class WebSocketClient:
    def __init__(self, danger: int = DENGERTHRESHOLD, warning: int =  WARNINGTHRESHOLD, name: str =  NAME, domain: str = DOMAIN, port: int = PORT,
                 secret_strategy = None,
                 estimate_strategy: estimate.EstimateStrategy = None,
                 challenge_candidate_strategy: candidate.ChallengeCandidateStrategy = None,
                 item_strategy: item.ItemStrategy = None):
        self._domain = domain
        self._port = port
        self._uri = f"ws://{self._domain}:{self._port}"
        self._initFlag = True
        self._danger = danger
        self._warning = warning
        self._name = name
        self._secret_strategy = secret_strategy
        self._estimate_strategy = estimate_strategy
        self._challenge_candidate_strategy = challenge_candidate_strategy
        self._item_strategy = item_strategy
        self._round = 0
        self._oppo_last_target = {
            "number": 0,
            "position": 0
        }
        self._oppo_last_challenge = {
            "number": "",
            "hit": 0,
            "blow": 0,
        }
        self.initForRound()

    def initForRound(self):
        self._estimate_strategy.setup()
        self._item_strategy.setup()
        self._secret = self._secret_strategy()
        self._answer_list = create_unique_list()
        self._answer_list_oppo = create_unique_list()
        self._trun_flag = 0
        self._can_use = True
        self._my_target = True
        self._my_highLow = True
        self._my_shuffle = True
        self._my_change = True
        self._oppo_target = True
        self._oppo_highLow = True
        self._oppo_shuffle = True
        self._oppo_change = True
        self._game_turn = 0
        self._round += 1
        self._oppo_last_target = {
                "number": 0,
            "position": 0
        }
        self._oppo_last_challenge = {
            "number": "",
            "hit": 0,
            "blow": 0,
        }
        print(f"round: {self._round}", file=sys.stderr)
        
    async def connect(self):
        async with websockets.connect(self._uri) as websocket:
            print(f"Connected to {self._uri}")
            try:
                async for message in websocket:
                    print(f"Received message: {message}")
                    await self.process_message(websocket, message)
            except websockets.ConnectionClosed:
                print("Connection closed")

    async def process_message(self, websocket, message: str):
        
        message = json.loads(message)
        message_type = message.get("messageType")

        if message_type == "requestPlayerName":
            response = PlayerNameResponse(name=self._name)
            await self.send(websocket, response.as_body())
        elif message_type == "requestSecretNumber":
            print(f"########################## NEW GAME round {self._round} #########################")
            response = SecretNumberResponse(number=self._secret)
            await self.send(websocket, response.as_body())
        elif message_type == "opponentActionResult":
            self._trun_flag = 0
            self._can_use = True
            action_obj = message.get("body").get("actionResults")
            for action in action_obj:
                if action.get("action") == "shuffle":
                    self._oppo_shuffle = False
                    self._answer_list = add_shuffle(self._answer_list)
                    
                elif action.get("action") == "change":
                    self._oppo_change = False
                    result_change = action.get("result")
                    result_change_position = result_change.get("position")
                    result_change_hl = result_change.get("high-low")
                    self._answer_list = add_change(self._answer_list, int(result_change_position), result_change_hl)
                    
                elif action.get("action") == "high-low":
                    self._oppo_highLow = False
                    result_high_low = action.get("result")
                    result_high = result_high_low.get("high")
                    result_low = result_high_low.get("low")
                    self._answer_list_oppo = delete_bad_answer_high_low(result_high, result_low, self._answer_list_oppo)
                elif action.get("action") == "target":
                    self._oppo_target = False
                    result_target = action.get("result")
                    result_target_number = result_target.get("number")
                    result_target_position = int(result_target.get("position"))
                    self._answer_list_oppo = delete_bad_answer_target(result_target_number, result_target_position, self._answer_list_oppo)
                    self._oppo_last_target = {
                        "number": int(result_target_number),
                        "position": int(result_target_position)
                    }
                elif action.get("action") == "challenge":
                    result_challenge = action.get("result")
                    result_challenge_number = result_challenge.get("number")
                    result_challenge_hit = result_challenge.get("hit")
                    result_challenge_blow = result_challenge.get("blow")
                    self._answer_list_oppo = delete_bad_answer(int(result_challenge_hit), int(result_challenge_blow), result_challenge_number, self._answer_list_oppo)
                    self._oppo_last_challenge = {
                        "number": result_challenge_number,
                        "hit": int(result_challenge_hit),
                        "blow": int(result_challenge_blow)
                    }
        elif message_type == "requestItemAction":
            if self._trun_flag == 0:
                self._game_turn += 1
            self._trun_flag += 1
            input = item.ItemStrategyInput(
                can_use_item=self._can_use,
                action_turn=self._trun_flag,
                answer_list_oppo=self._answer_list_oppo,
                secret=self._secret,
                game_turn=self._game_turn,
                answer_list=self._answer_list,
                can_oppo_use_shuffle=self._oppo_shuffle,
                can_oppo_use_target=self._oppo_target,
                oppo_last_target=self._oppo_last_target,
                oppo_lash_challenge=self._oppo_last_challenge,
            )
            output = self._item_strategy.execute(input)
            if output.did_use_item():
                self._can_use = False
            if output.new_secret is not None:
                self._secret = output.new_secret
            if output.new_answer_list_oppo is not None:
                self._answer_list_oppo = output.new_answer_list_oppo
            await self.send(websocket, output.as_body())

        elif message_type == "itemActionResult-high-low":
            result_high_low = message.get("body").get("result")
            result_high = result_high_low.get("high")
            result_low = result_high_low.get("low")
            self._answer_list = delete_bad_answer_high_low(result_high, result_low, self._answer_list)
        elif message_type == "itemActionResult-target":
            result_target = message.get("body").get("result")
            result_target_number = result_target.get("number")
            result_target_position = int(result_target.get("position"))
            self._answer_list = delete_bad_answer_target(result_target_number, result_target_position, self._answer_list)
        elif message_type == "requestChallengeNumber":
            input = estimate.EstimateInput(
                answer_list=self._answer_list,
                challenge_candidates=self._challenge_candidate_strategy.candidates(
                    candidate.ChallengeCandidateInput(
                        answer_list=self._answer_list,
                        game_turn=self._game_turn
                    )
                ),
                answer_list_oppo=self._answer_list_oppo,
            )
            response = ChallengeNumberResponse(self._estimate_strategy.estimate(input))
            await self.send(websocket, response.as_body())
        elif message_type == "challengeResult":
            result_obj = message.get("body").get("result")
            result_number = result_obj.get("number")
            result_hit = int(result_obj.get("hit"))
            result_blow = int(result_obj.get("blow"))
            self._answer_list = delete_bad_answer(result_hit, result_blow, result_number, self._answer_list)
            print(f"feedback: {result_hit}H{result_blow}B, answers: {len(self._answer_list)}", file=sys.stderr)
            self._estimate_strategy.on_feedback(declared_number=result_number, feedback=f"${result_hit}H${result_blow}B")
        elif message_type == "roundResult":
            self._estimate_strategy.teardown()
            print("\n###################################################\n", file=sys.stderr)
            self.initForRound();
        elif message_type == "tellPlayerNumber":
            self._player_number = message.get("body").get("playerNumber")

            
            
    async def send(self, websocket, message):
        print(f"Send message: {message}")
        await websocket.send(json.dumps(message))


    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect())

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="WebSocket Client")
    parser.add_argument("--d", type=int, default=200, help="Danger threshold")
    parser.add_argument("--w", type=int, default=1500,help="Warning threshold")
    parser.add_argument("--n", type=str, default="noname",help="Name")
    parser.add_argument("--secret", type=str, default="hhll", help="Secret strategy")
    parser.add_argument("--estimate", type=str, default="blandy", help="Estimate strategy")
    parser.add_argument("--candidate", type=str, default="pick_from_answer", help="Challenge candidate strategy")
    parser.add_argument("--item", type=str, default="default", help="Item strategy")
    args = parser.parse_args()
    print(f"Arguments: {args}")
    client = WebSocketClient(args.d, args.w, args.n,
        secret_strategy=secret.factory_secret_strategy(args.secret),
        estimate_strategy=estimate.factory_estimate_strategy(args.estimate),
        challenge_candidate_strategy=candidate.factory_challenge_candidate_strategy(args.candidate),
        item_strategy=item.factory_item_strategy(args.item),
    )
    client.start()
