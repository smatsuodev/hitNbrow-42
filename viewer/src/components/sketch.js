const sketch = (p) => {
  let points = [];
  let tickSpeed = 2;
  let base = 180;
  let numPoints = 10;
  let maxTicks = 2000;
  let ticks = 0;

  class Point {
    constructor(x = p.random(p.width), y = p.random(p.height), a = p.random(p.PI)) {
      this.x = x;
      this.y = y;
      this.a = a;
      this.dx = p.cos(a);
      this.dy = p.sin(a);
      this.hue = (p.random(100) + base) % 360;
      this.color = p.color(this.hue, 100, 100, 0.01);
    }

    update() {
      this.x += this.dx;
      this.y += this.dy;
      if (this.x < 0 || this.x >= p.width) this.dx *= -1;
      if (this.y < 0 || this.y >= p.height) this.dy *= -1;
      p.stroke(this.color);
      p.line(this.x, this.y, this.neighbor.x, this.neighbor.y);
    }
  }

  p.setup = () => {
    p.createCanvas(p.windowWidth, p.windowHeight);
    p.colorMode(p.HSB);
    p.blendMode(p.ADD);
    p.strokeWeight(1.5);
    init();
  };

  const init = () => {
    // 初期化処理
    points = [];
    base = p.random(360);
    ticks = 0;

    for (let i = 0; i < numPoints; i++) points.push(new Point());

    for (let i = 0; i < points.length; i++) {
      let j = i;
      while (j === i) j = Math.floor(p.random(points.length));
      points[i].neighbor = points[j];
    }

    // 画面をクリアして背景を設定
    p.clear();
    p.background(0);
  };

  p.draw = () => {
    if (ticks > maxTicks) {
      // 描画終了後にX秒後に再実行
      setTimeout(() => {
        init();
      }, 20000);
      ticks = 0; // 次回描画のためにカウンターをリセット
      return;
    }

    for (let n = 0; n < tickSpeed; n++) {
      points.forEach((point) => point.update());
      ticks++;
    }
  };

  p.mouseClicked = () => {
    init();
  };

  p.windowResized = () => {
    p.resizeCanvas(p.windowWidth, p.windowHeight);
    p.pixelDensity(1);
    init();
  };
};

export default sketch;
