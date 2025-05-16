
import React from "react";

function WinnerScreen({ winner }) {
  return (
    <div className="winner-screen relative flex items-center justify-center min-h-screen bg-gradient-to-br from-black to-gray-900 text-white">
      <div className="absolute inset-0 overflow-hidden z-0">
        <div className="absolute w-[30rem] h-[30rem] border-4 border-yellow-500 rounded-full animate-pulse opacity-30 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"></div>
      </div>

      <div className="relative z-10 text-center">
        <h1 className="text-5xl md:text-7xl font-bold text-yellow-400 drop-shadow-lg">
          {winner.name && "Congratulations!"}
        </h1>
        <p className="text-4xl md:text-6xl font-bold mt-4 text-white drop-shadow">
          {winner.name || "DRAW"}
        </p>
        <p className="text-3xl md:text-5xl font-bold mt-4 text-white drop-shadow">
          {/* Points: {winner.points} */}
        </p>
        <div className="mt-8">
          {winner.name && 
            <img
              src="/images/trophy.png"
              className="w-64 h-64 md:w-96 md:h-96 mx-auto"
            />
          }
        </div>
      </div>
    </div>
  );
}

export default WinnerScreen;
