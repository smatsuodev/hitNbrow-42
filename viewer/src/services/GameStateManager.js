import { WS_URL } from '../utils/constants';

class GameStateManager {
  constructor(setGameState) {
    this.setGameState = setGameState;
    this.socket = null;
  }

  connect() {
    this.socket = new WebSocket(WS_URL);
    this.socket.onmessage = (e) => this.handleMessage(e);
    this.socket.onopen = () => console.log("WebSocket connected.");
    this.socket.onclose = () => console.log("WebSocket disconnected.");
    this.socket.onerror = (error) => console.error("WebSocket error:", error);
  }

  // WebSocket接続を切断
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  handleMessage(event) {
    console.log("onmessage");
    try {
      const data = JSON.parse(event.data);
      console.log(data);
      if (
        ["matching", "start-game", "in-game", "finish-game"].includes(data.state)
      ) {
        switch (data.messageType) {
          case "sendPlayerName":
            this.handlePlayerList(data.body);
            break;
          case "sendSecretNumber":
            this.handlePlayerNumbers(data.body);
            break;
          case "challengeResult":
          case "itemActionResult-target":
          case "itemActionResult-high-low":
          case "itemActionResult-shuffle":
          case "itemActionResult-change":
            this.handleActionResult(data.body);
            break;
          case "itemActionResult-pass":
            break;
          case "roundResult":
            this.handleRoundResult(data.body);
            break;
          case "gameResult":
            this.handleGameResult(data.body);
            break;
          default:
            console.warn("Unknown message type:", data.message);
        }
      } else {
        console.warn("Invalid message format:", data);
      }
    } catch (error) {
      console.error("Error processing WebSocket message:", error);
    }
  }

  handlePlayerList(body) {
    const playerList = body.players;
    const updatedPlayer1 = playerList.find(player => player.playerNumber === 1);
    const updatedPlayer2 = playerList.find(player => player.playerNumber === 2);
  
    this.setGameState((prevState) => ({
      ...prevState,
      player1: { 
        ...prevState.player1, 
        name: updatedPlayer1 ? `${updatedPlayer1.playerName}\n` : prevState.player1.playerName
      },
      player2: { 
        ...prevState.player2, 
        name: updatedPlayer2 ? `${updatedPlayer2.playerName}\n` : prevState.player2.playerName
      },
    }));
  }

  // ナンバー通知の処理
  handlePlayerNumbers(body) {
    const numbers = body.secrets;
    this.setGameState((prevState) => {
      const player1Number = numbers.find(n => n.playerNumber === 1)?.number?.split('') || ["", "", "", ""];
      const player2Number = numbers.find(n => n.playerNumber === 2)?.number?.split('') || ["", "", "", ""];
      
      return {
        ...prevState,
        player1: {
          ...prevState.player1,
          selected: player1Number
        },
        player2: {
          ...prevState.player2,
          selected: player2Number
        }
      };
    });
  }

  // アクション結果の処理
  handleActionResult(result) {
    this.setGameState((prevState) => {
      const targetPlayer = result.playerNumber === 1 ? 'player1' : 'player2';
      const updatedState = { ...prevState };
      
      // アクションポイントの更新
      updatedState[targetPlayer] = {
        ...updatedState[targetPlayer],
        ap: result.actionPoint
      };

      // アクション種別に応じた処理
      switch (result.action) {
        case "challenge": {
          const { number, hit, blow } = result.result;
          updatedState[targetPlayer] = {
            ...updatedState[targetPlayer],
            chose: number.split(''),
            result: {
              hit: hit,
              blow: blow
            },
            history: [
              ...updatedState[targetPlayer].history, 
              `${number} H:${hit} B:${blow}`
            ]
          };
          break;
        }
        case "high-low": {
          const { high, low } = result.result;
          updatedState[targetPlayer] = {
            ...updatedState[targetPlayer],
            items: updatedState[targetPlayer].items.filter(item => item !== result.action),
            history: [
              ...updatedState[targetPlayer].history, 
              `high-low h:${high} l:${low}`
            ],
          };
          break;
        }
        case "shuffle":
        case "change": {
          const { number } = result.result;
          const oldSelected = updatedState[targetPlayer].selected.join('');
          const newSelected = number.split('');
        
          updatedState[targetPlayer] = {
            ...updatedState[targetPlayer],
            selected: newSelected,
            items: updatedState[targetPlayer].items.filter(item => item !== result.action),
            history: [
              ...updatedState[targetPlayer].history,
              `${result.action} ${oldSelected}⇒${newSelected.join('')}`
            ],
          };
          break;
        }
        case "target": {
          const { number, position } = result.result;

          const historyEntry = `target N:${number} P:${position}`;

          updatedState[targetPlayer] = {
            ...updatedState[targetPlayer],
            items: updatedState[targetPlayer].items.filter(item => item !== result.action),
            history: [
              ...updatedState[targetPlayer].history,
              historyEntry
            ],
          };
          break;
        }
      }
      return updatedState;
    });
  }

  // ラウンド終了時の処理
  handleRoundResult(result) {
    const winnerPlayerNumber = result.winnerPlayerNumber;
    
    this.setGameState((prevState) => {
      const updatedPlayer1Name = 
        winnerPlayerNumber === 1 
          ? `${prevState.player1.name} ★` 
          : prevState.player1.name;
  
      const updatedPlayer2Name = 
        winnerPlayerNumber === 2 
          ? `${prevState.player2.name} ★` 
          : prevState.player2.name;
  
      return {
        ...prevState,
        player1: {
          ...prevState.player1,
          name: updatedPlayer1Name,
          selected: ["", "", "", ""],
          chose: ["", "", "", ""],
          result: { hit: 0, blow: 0 },
          history: [],
          ap: 20,
          items: ["high-low", "shuffle", "change", "target"],
        },
        player2: {
          ...prevState.player2,
          name: updatedPlayer2Name,
          selected: ["", "", "", ""],
          chose: ["", "", "", ""],
          result: { hit: 0, blow: 0 },
          history: [],
          ap: 20,
          items: ["high-low", "shuffle", "change", "target"],
        },
      };
    });
  }

  // ゲーム終了時の処理
  handleGameResult(result) {
    let winnerPlayer = "draw";
    if (result.winnerPlayerNumber === 1) winnerPlayer = "player1";
    if (result.winnerPlayerNumber === 2) winnerPlayer = "player2";

    this.setGameState((prevState) => ({
      ...prevState,
      winner: {
        name: prevState[winnerPlayer].name.split("\n")[0],
        points: result.points,
      },
      gameEnded: true,
    }));
  }
}

export default GameStateManager;
