import React, { useEffect, useRef } from 'react';
import p5 from 'p5';
import sketch from './sketch';
import '../background.css';

const Background = () => {
  const containerRef = useRef(null);

  useEffect(() => {
    const p5Instance = new p5(sketch, containerRef.current); // containerRef に紐付け
    return () => p5Instance.remove();
  }, []);

  return <div className="background-container" ref={containerRef} />;
};

export default Background;
