import argparse
import asyncio
import websockets
import json



from player.sendMessage.ChallengeNumberResponse import ChallengeNumberResponse
from player.sendMessage.ItemActionPassResponse import ItemActionPassResponse
from player.sendMessage.PlayerNameResponse import PlayerNameResponse
from player.sendMessage.SecretNumberResponse import SecretNumberResponse
from util.commonUtils import add_change, addSuffle, delete_bad_answer, delete_bad_answer_high_low, delete_bad_answer_target, do_change, do_suffle, generate_unique_numbers, create_unique_list
from strategy import secret

DOMAIN = 'localhost'
PORT = 8088
NAME = 'JO'
DENGERTHRESHOLD = 500
WARNINGTHRESHOLD = 1000



class WebSocketClient:
    def __init__(self, danger: int = DENGERTHRESHOLD, warning: int =  WARNINGTHRESHOLD, name: str =  NAME, domain: str = DOMAIN, port: int = PORT, secret_strategy = generate_unique_numbers):
        self._domain = domain
        self._port = port
        self._uri = f"ws://{self._domain}:{self._port}"
        self._initFlag = True
        self._danger = danger
        self._warning = warning
        self._name = name
        self._secret_strategy = secret_strategy
        self.initForRound()

    def initForRound(self):
        self._secret = self._secret_strategy()
        self._answerList = create_unique_list()
        self._answerList_oppo = create_unique_list()
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
                    self._answerList = addSuffle(self._answerList)
                    
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
                    self._answerList_oppo = delete_bad_answer_high_low(result_high, result_low, self._answerList_oppo)
                elif action.get("action") == "target":
                    self._oppo_target = False
                    result_target = action.get("result")
                    result_target_number = result_target.get("number")
                    result_target_position = result_target.get("position")
                    self._answerList_oppo = delete_bad_answer_target(result_target_number, result_target_position, self._answerList_oppo)
                elif action.get("action") == "challenge":
                    result_challenge = action.get("result")
                    result_challenge_number = result_challenge.get("number")
                    result_challenge_hit = result_challenge.get("hit")
                    result_challenge_blow = result_challenge.get("blow")
                    self._answerList_oppo = delete_bad_answer(result_challenge_hit, result_challenge_blow, result_challenge_number, self._answerList_oppo)
        elif message_type == "requestItemAction":
            self._trun_flag += 1
            if (self._can_use and self._trun_flag == 1):
                if (self._my_highLow):
                    response = {
                        "messageType": 'requestItemAction-high-low',
                        "body": {
                            "action":"high-low",
                        }
                    }
                    await self.send(websocket, response)
                    self._my_highLow = False
                    self._can_use = False
                    return
                elif (self._my_target):
                    response = {
                        "messageType": 'requestItemAction-target',
                        "body": {
                            "action":"target",
                            "number": "5",
                        }
                    }
                    await self.send(websocket, response)
                    self._my_target = False
                    self._can_use = False
                    return
            elif (self._can_use and self._trun_flag == 2):
                if len(self._answerList_oppo) <= self._danger and self._my_change:
                    [new_secret, i, highlow] = do_change(self._answerList_oppo, self._secret)
                    self._secret = new_secret
                    response = {
                        "messageType": 'requestItemAction-change',
                        "body": {
                            "action":"change",
                            "number":self._secret,
                        }
                    }
                    await self.send(websocket, response)
                    self._answerList_oppo = add_change(self._answerList_oppo, i, highlow)
                    self._my_change = False
                    self._can_use = False
                    return  
                if len(self._answerList_oppo) <= self._warning and self._my_shuffle:
                    self._secret = do_suffle(self._secret)
                    response = {
                        "messageType": 'requestItemAction-shuffle',
                        "body": {
                            "action":"shuffle",
                            "number":self._secret,
                        }
                    }
                    await self.send(websocket, response)
                    self._answerList_oppo = addSuffle(self._answerList_oppo)
                    self._my_shuffle = False
                    self._can_use = False
                    return  
            response = ItemActionPassResponse()
            await self.send(websocket, response.as_body())
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
            response = ChallengeNumberResponse(self._answerList[0])
            await self.send(websocket, response.as_body())
        elif message_type == "challengeResult":
            result_obj = message.get("body").get("result")
            result_number = result_obj.get("number")
            result_hit = result_obj.get("hit")
            result_blow = result_obj.get("blow")
            self._answerList = delete_bad_answer(result_hit, result_blow, result_number, self._answerList)
        elif message_type == "roundResult":
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
    client = WebSocketClient(args.d, args.w, args.n, secret_strategy=secret.gen_h2l2)
    client.start()
