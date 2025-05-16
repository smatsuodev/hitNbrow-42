import React from 'react';
import './background.css';
import MainComponent from './components/MainComponent';
import Background from './components/Background';

function App() {
  return (
    <div className="App">
      {/* 背景アニメーション */}
      <Background />
      
      {/* メインコンポーネント */}
      <MainComponent />
    </div>
  );
}

export default App;
