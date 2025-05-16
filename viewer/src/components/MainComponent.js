import React from 'react';
import { ITEM_IMAGES } from "../utils/constants";
import GameStateManager from '../services/GameStateManager';
import WinnerScreen from './WinnerScreen';

 // 検証用
 import MockWebSocket from "../utils/MockWebSocket";


function MainComponent() {
  // ゲームの状態管理
  const [gameState, setGameState] = React.useState({
    player1: {
      name: "",
      selected: ["", "", "", ""],
      chose: ["", "", "", ""],
      result: { hit: 0, blow: 0},
      history: [],
      ap: 20,
      items: ["high-low", "shuffle", "change", "target"]
    },
    player2: {
      name: "",
      selected: ["", "", "", ""],
      chose: ["", "", "", ""],
      result: { hit: 0, blow: 0},
      history: [],
      ap: 20,
      items: ["high-low", "shuffle", "change", "target"]
    },
    draw: {
      name: ""
    },
    winner: null,
    gameEnded: false,
  });

  const gameStateManagerRef = React.useRef(null);

  // websocket用
  React.useEffect(() => {
    gameStateManagerRef.current = new GameStateManager(setGameState);
    gameStateManagerRef.current.connect();
    return () => {
      gameStateManagerRef.current.disconnect();
      gameStateManagerRef.current = null;
    };
  }, []);

  // 検証用
  // React.useEffect(() => {
  //   gameStateManagerRef.current = new GameStateManager(setGameState);
  //   const mockWebSocket = new MockWebSocket((message) => {
  //     gameStateManagerRef.current.handleMessage(message);
  //   });
  //   mockWebSocket.startSimulation();
  // }, []);


  return (
    <div className="relative z-10 bg-black/45 text-white min-h-screen flex flex-col md:flex-row">
      {gameState.gameEnded ? (
        <WinnerScreen winner={gameState.winner} />
      ) : (
        <>
          <div className="w-full md:w-[160px] p-2 md:p-4 md:mt-64 bg-[#1a1a1a]">
            <h3 className="text-lg md:text-xl mb-2 md:mb-4 text-center">CALL</h3>
            <ul>
              {gameState.player1.history.map((item, index) => (
                <li key={index} className="mb-1 md:mb-2 text-sm md:text-lg text-center">
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div className="flex-1 flex flex-col">
            <div className="text-center py-2 md:py-4">
              <h1 className="text-3xl md:text-5xl font-bold">SMARTSCAPE CUP</h1>
            </div>
            <div className="flex h-16 md:h-24 mb-4 md:mb-8">
              <PlayerHeader player={gameState.player1.name} color="bg-blue-600" isLeft={true} />
              <PlayerHeader player={gameState.player2.name} color="bg-red-600" isLeft={false} />
            </div>
            <div className="flex-1 flex flex-col md:flex-row">
              <PlayerSection
                selectedNumbers={gameState.player1.selected}
                choseNumbers={gameState.player1.chose}
                isLeft={true}
                result={gameState.player1.result}
                ap={gameState.player1.ap}
                items={gameState.player1.items}
              />
              <PlayerSection
                selectedNumbers={gameState.player2.selected}
                choseNumbers={gameState.player2.chose}
                isLeft={false}
                result={gameState.player2.result}
                ap={gameState.player2.ap}
                items={gameState.player2.items}
              />
            </div>
          </div>

          <div className="w-full md:w-[160px] p-2 md:p-4 md:mt-64 bg-[#1a1a1a]">
            <h3 className="text-lg md:text-xl mb-2 md:mb-4 text-center">CALL</h3>
            <ul>
              {gameState.player2.history.map((item, index) => (
                <li key={index} className="mb-1 md:mb-2 text-sm md:text-lg text-center">
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}

function PlayerHeader({ player, color, isLeft }) {
  return (
    <div
      className={`flex-1 h-full relative overflow-hidden ${
        isLeft ? "text-left" : "text-right"
      }`}
    >
      <div
        className={`${color} absolute inset-0 ${
          isLeft ? "origin-bottom-left" : "origin-bottom-right"
        }`}
        style={{
          clipPath: isLeft
            ? "polygon(5% 0, 85% 0, 95% 100%, 15% 100%)"
            : "polygon(15% 0, 95% 0, 85% 100%, 5% 100%)",
        }}
      ></div>
      <div className="absolute inset-0 flex items-center justify-center px-8 md:px-16">
        <h2 className="text-2xl md:text-4xl font-bold z-10 text-center">
          {(player ?? "").split("\n").map((line, index) => (
            <React.Fragment key={index}>
              <div>{line}</div>
              {index < (player.split("\n").length - 1)}
            </React.Fragment>
          ))}
        </h2>
      </div>
    </div>
  );
}

function PlayerSection({
  selectedNumbers,
  choseNumbers,
  isLeft,
  result,
  ap,
  items,
}) {
  return (
    <div className="flex-1 p-2 md:p-4 flex flex-col items-center">
      <div className={`flex flex-col md:flex-row ${isLeft ? '' : 'md:flex-row-reverse'} gap-4 md:gap-8`}>
        <div className="flex flex-col items-center">
          <h3 className="text-xl md:text-3xl font-bold mb-2">Selected Number</h3>
          <div className="flex space-x-2 md:space-x-2">
            {selectedNumbers.map((num, index) => (
              <div
                key={index}
                className="w-12 h-16 md:w-16 md:h-28 border-2 md:border-4 border-white bg-black text-white flex items-center justify-center text-2xl md:text-4xl font-bold"
              >
                {num}
              </div>
            ))}
          </div>
        </div>
        <div className="flex flex-col items-center">
          <h3 className="text-xl md:text-3xl font-bold mb-2">Items</h3>
          <div
            className="grid grid-cols-2 md:grid-cols-2 gap-1 md:gap-2"
            style={{
              gridTemplateRows: "repeat(2, auto)",
              height: "100px",
            }}
          >
            {items.map((item, index) => (
              <div key={index} className="w-12 h-12 md:w-16 md:h-16">
                <img
                  src={ITEM_IMAGES[item]}
                  alt={`アイテム${item}`}
                  className="w-full h-full object-cover"
                />
              </div>
            ))}
            {Array.from({ length: 4 - items.length }).map((_, index) => (
              <div key={`empty-${index}`} className="w-12 h-12 md:w-16 md:h-16"></div>
            ))}
          </div>
        </div>
      </div>

      {/* <div className="text-2xl md:text-4xl">AP : {ap}</div> */}

      <div className="w-full max-w-md mt-2 md:mt-4">
        <div className="flex justify-between items-center mb-3 md:mb-6">
          <h3 className="text-2xl md:text-4xl ml-10 md:ml-20">Choose Number</h3>
        </div>
        <div className="flex justify-center space-x-2 md:space-x-4">
          {choseNumbers.map((num, index) => (
            <div
              key={index}
              className="w-20 h-32 md:w-32 md:h-48 border-2 md:border-4 border-white bg-black text-white flex items-center justify-center text-5xl md:text-7xl font-bold"
            >
              {num}
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-center space-x-4 md:space-x-8 mt-4 md:mt-8 w-full max-w-xs">
        <div className="text-2xl md:text-4xl">HIT</div>
        <div className="text-2xl md:text-4xl">{result.hit}</div>
        <div className="text-2xl md:text-4xl">BLOW</div>
        <div className="text-2xl md:text-4xl">{result.blow}</div>
      </div>
    </div>
  );
}

export default MainComponent;