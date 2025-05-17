import argparse
import asyncio
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

DOMAIN = '10.18.239.70'
PORT = 8088
NAME = 'JO'
DENGERTHRESHOLD = 500
WARNINGTHRESHOLD = 1000
SECRET_STRATEGY = secret.gen_h2l2
ESTIMATE_STRATEGY = estimate.MutualInfoStrategy()
CHALLENGE_CANDIDATE_STRATEGY = candidate.PickFromAnswerStrategy()
ITEM_STRATEGY = item.DefaultItemStrategy(danger=DENGERTHRESHOLD, warning=WARNINGTHRESHOLD)


class WebSocketClient:
    def __init__(self, danger: int = DENGERTHRESHOLD, warning: int =  WARNINGTHRESHOLD, name: str =  NAME, domain: str = DOMAIN, port: int = PORT,
                 secret_strategy = SECRET_STRATEGY,
                 estimate_strategy: estimate.EstimateStrategy = ESTIMATE_STRATEGY,
                 challenge_candidate_strategy: candidate.ChallengeCandidateStrategy = CHALLENGE_CANDIDATE_STRATEGY,
                 item_strategy: item.ItemStrategy = ITEM_STRATEGY):
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
        self.initForRound()

    def initForRound(self):
        self._estimate_strategy.setup()
        self._item_strategy.setup()
        self._secret = self._secret_strategy()
        self._answerList = create_unique_list()
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
            print(f"########################## NEW GAME #########################")
            response = SecretNumberResponse(number=self._secret)
            await self.send(websocket, response.as_body())
        elif message_type == "opponentActionResult":
            self._trun_flag = 0
            self._can_use = True
            action_obj = message.get("body").get("actionResults")
            for action in action_obj:
                if action.get("action") == "shuffle":
                    self._oppo_shuffle = False
                    self._answerList = add_shuffle(self._answerList)
                    
                elif action.get("action") == "change":
                    self._oppo_change = False
                    result_change = action.get("result")
                    result_change_position = result_change.get("position")
                    result_change_hl = result_change.get("high-low")
                    self._answerList = add_change(self._answerList, int(result_change_position), result_change_hl)
                    
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
                    result_target_position = result_target.get("position")
                    self._answer_list_oppo = delete_bad_answer_target(result_target_number, result_target_position, self._answer_list_oppo)
                elif action.get("action") == "challenge":
                    result_challenge = action.get("result")
                    result_challenge_number = result_challenge.get("number")
                    result_challenge_hit = result_challenge.get("hit")
                    result_challenge_blow = result_challenge.get("blow")
                    self._answer_list_oppo = delete_bad_answer(result_challenge_hit, result_challenge_blow, result_challenge_number, self._answer_list_oppo)
        elif message_type == "requestItemAction":
            self._trun_flag += 1
            input = item.ItemStrategyInput(
                can_use_item=self._can_use,
                turn=self._trun_flag,
                answer_list_oppo=self._answer_list_oppo,
                secret=self._secret,
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
            self._answerList = delete_bad_answer_high_low(result_high, result_low, self._answerList)
        elif message_type == "itemActionResult-target":
            result_target = message.get("body").get("result")
            result_target_number = result_target.get("number")
            result_target_position = result_target.get("position")
            self._answerList = delete_bad_answer_target(result_target_number, result_target_position, self._answerList)
        elif message_type == "requestChallengeNumber":
            input = estimate.EstimateInput(
                answerList=self._answerList,
                challengeCandidates=self._challenge_candidate_strategy.candidates(
                    candidate.ChallengeCandidateInput(answerList=self._answerList)
                )
            )
            response = ChallengeNumberResponse(self._estimate_strategy.estimate(input))
            await self.send(websocket, response.as_body())
        elif message_type == "challengeResult":
            result_obj = message.get("body").get("result")
            result_number = result_obj.get("number")
            result_hit = result_obj.get("hit")
            result_blow = result_obj.get("blow")
            self._answerList = delete_bad_answer(result_hit, result_blow, result_number, self._answerList)
        elif message_type == "roundResult":
            self._estimate_strategy.teardown()
            self.initForRound();
            
            
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
    args = parser.parse_args()
    client = WebSocketClient(args.d, args.w, args.n)
    client.start()
