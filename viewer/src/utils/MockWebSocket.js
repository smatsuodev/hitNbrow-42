class MockWebSocket {
  constructor(onMessage) {
    this.onMessage = onMessage;
  }

  startSimulation() {
    // ゲーム開始
    setTimeout(() => {
      this.onMessage({
        data: JSON.stringify({
          state: "matching",
          messageType: "message",
          message: "player list",
          body: [
            { playerNumber: 1, playerName: "test1" },
            { playerNumber: 2, playerName: "test2" },
          ],
        }),
      });
    }, 1000);

    // 1試合目
    setTimeout(() => {
      this.onMessage({
        data: JSON.stringify({
          state: "start-game",
          messageType: "message",
          message: "player numbers",
          body: [
            { playerNumber: 1, number: "5678" },
            { playerNumber: 2, number: "3456" }
          ]
      })});
    }, 4000);

    setTimeout(() => {
      this.onMessage({
        data: JSON.stringify({
          state: "in-game",
          messageType: "message",
          message: "action result",
          body: {
            playerNumber: 1,
            action: "call",
            actionPoint: 19,
            result: {
              callNumber: "1236",
              hit: 1,
              blow: 1
            }
          }
      })});
    }, 7000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 2,
          action: "call",
          actionPoint: 19,
          result: {
            callNumber: "1236",
            hit: 0,
            blow: 1
          }
        }
      })});
    }, 10000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 1,
          action: "call",
          actionPoint: 18,
          result: {
            callNumber: "3412",
            hit: 2,
            blow: 0
          }
        }
      })});
    }, 13000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 2,
          action: "call",
          actionPoint: 18,
          result: {
            callNumber: "5679",
            hit: 3,
            blow: 0
          }
        }
      })});
    }, 16000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 1,
          action: "high-low",
          actionPoint: 17,
          result: {
            high: 2,
            low: 2
          }
        }
      })});
    }, 19000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 1,
          action: "call",
          actionPoint: 16,
          result: {
            callNumber: "1298",
            hit: 0,
            blow: 0
          }
        }
      })});
    }, 22000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 2,
          action: "shuffle",
          actionPoint: 17,
          result: "6534"
        }
      })});
    }, 25000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 2,
          action: "call",
          actionPoint: 16,
          result: {
            callNumber: "5674",
            hit: 3,
            blow: 0
          }
        }
      })});
    }, 28000);


    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 1,
          action: "change",
          actionPoint: 15,
          result: "4678"
        }
      })});
    }, 31000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 1,
          action: "call",
          actionPoint: 14,
          result: {
            callNumber: "1298",
            hit: 0,
            blow: 0
          }
        }
      })});
    }, 34000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 2,
          action: "target",
          actionPoint: 15,
          result: {
            number: "8",
            position: 4
          }
        }
      })});
    }, 37000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 2,
          action: "call",
          actionPoint: 14,
          result: {
            callNumber: "5674",
            hit: 2,
            blow: 0
          }
        }
      })});
    }, 40000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "in-game",
        messageType: "message",
        message: "action result",
        body: {
          playerNumber: 1,
          action: "call",
          actionPoint: 13,
          result: {
            callNumber: "6534",
            hit: 4,
            blow: 0
          }
        }
      })});
    }, 43000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "round-end",
        messageType: "message",
        message: "round result",
        body: {
          playerNumber: 1,
          points: 13
        }
      })});
    }, 45000);

    // 2試合目
    setTimeout(() => {
      this.onMessage({
        data: JSON.stringify({
          state: "start-game",
          messageType: "message",
          message: "player numbers",
          body: [
            { playerNumber: 1, number: "1234" },
            { playerNumber: 2, number: "2345" }
          ]
      })});
    }, 48000);

    setTimeout(() => {
      this.onMessage({
        data: JSON.stringify({
          state: "in-game",
          messageType: "message",
          message: "action result",
          body: {
            playerNumber: 2,
            action: "call",
            actionPoint: 19,
            result: {
              callNumber: "1234",
              hit: 4,
              blow: 0
            }
          }
      })});
    }, 51000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "round-end",
        messageType: "message",
        message: "round result",
        body: {
          playerNumber: 2,
          points: 19
        }
      })});
    }, 54000);


    // 3試合目
    setTimeout(() => {
      this.onMessage({
        data: JSON.stringify({
          state: "start-game",
          messageType: "message",
          message: "player numbers",
          body: [
            { playerNumber: 1, number: "4567" },
            { playerNumber: 2, number: "9876" }
          ]
      })});
    }, 57000);

    setTimeout(() => {
      this.onMessage({
        data: JSON.stringify({
          state: "in-game",
          messageType: "message",
          message: "action result",
          body: {
            playerNumber: 1,
            action: "call",
            actionPoint: 19,
            result: {
              callNumber: "9876",
              hit: 4,
              blow: 0
            }
          }
      })});
    }, 60000);

    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "round-end",
        messageType: "message",
        message: "round result",
        body: {
          playerNumber: 1,
          points: 19
        }
      })});
    }, 63000);

    // ゲーム終了
    setTimeout(() => {
      this.onMessage({data: JSON.stringify({
        state: "game-end",
        messageType: "message",
        message: "game result",
        body: {
          playerNumber: 1,
          points: 32
        }
      })});
    }, 66000);

  }
}

export default MockWebSocket;
