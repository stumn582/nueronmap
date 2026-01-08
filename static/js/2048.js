const size = 4;
let board = [];
let score = 0;
let gameEnded = false;

/* ======================
   초기화
====================== */
function initGame() {
  board = Array(size * size).fill(0);
  score = 0;
  gameEnded = false;

  addTile();
  addTile();
  render();
}

/* ======================
   타일 추가
====================== */
function addTile() {
  const empty = board
    .map((v, i) => (v === 0 ? i : null))
    .filter(v => v !== null);

  if (empty.length === 0) return;

  const index = empty[Math.floor(Math.random() * empty.length)];
  board[index] = Math.random() < 0.9 ? 2 : 4;
}

/* ======================
   렌더링
====================== */
function render() {
  const container = document.getElementById("game-container");
  container.innerHTML = "";

  board.forEach(value => {
    const tile = document.createElement("div");
    tile.className = "tile";

    if (value > 0) {
      tile.textContent = value;
      tile.classList.add("tile-" + value);
    }

    container.appendChild(tile);
  });
}

/* ======================
   슬라이드 로직
====================== */
function slide(row) {
  row = row.filter(v => v !== 0);

  for (let i = 0; i < row.length - 1; i++) {
    if (row[i] === row[i + 1]) {
      row[i] *= 2;
      score += row[i];
      row[i + 1] = 0;
    }
  }

  row = row.filter(v => v !== 0);
  while (row.length < size) row.push(0);

  return row;
}

/* ======================
   이동 로직
====================== */
function moveLeft() {
  let moved = false;
  for (let r = 0; r < size; r++) {
    const row = board.slice(r * size, r * size + size);
    const newRow = slide(row);
    if (row.toString() !== newRow.toString()) moved = true;
    board.splice(r * size, size, ...newRow);
  }
  return moved;
}

function moveRight() {
  let moved = false;
  for (let r = 0; r < size; r++) {
    const row = board.slice(r * size, r * size + size).reverse();
    const newRow = slide(row).reverse();
    if (row.reverse().toString() !== newRow.toString()) moved = true;
    board.splice(r * size, size, ...newRow);
  }
  return moved;
}

function moveUp() {
  let moved = false;
  for (let c = 0; c < size; c++) {
    let col = [];
    for (let r = 0; r < size; r++) col.push(board[r * size + c]);

    const newCol = slide(col);

    for (let r = 0; r < size; r++) {
      if (board[r * size + c] !== newCol[r]) moved = true;
      board[r * size + c] = newCol[r];
    }
  }
  return moved;
}

function moveDown() {
  let moved = false;
  for (let c = 0; c < size; c++) {
    let col = [];
    for (let r = size - 1; r >= 0; r--) col.push(board[r * size + c]);

    const newCol = slide(col).reverse();

    for (let r = 0; r < size; r++) {
      if (board[r * size + c] !== newCol[r]) moved = true;
      board[r * size + c] = newCol[r];
    }
  }
  return moved;
}

/* ======================
   게임 오버 판별
====================== */
function isGameOver() {
  if (board.includes(0)) return false;

  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      const v = board[r * size + c];
      if (
        (c < size - 1 && v === board[r * size + c + 1]) ||
        (r < size - 1 && v === board[(r + 1) * size + c])
      ) {
        return false;
      }
    }
  }
  return true;
}

/* ======================
   키 이벤트
====================== */
document.addEventListener("keydown", e => {
  if (gameEnded) return;

  let moved = false;

  if (e.key === "ArrowLeft") moved = moveLeft();
  if (e.key === "ArrowRight") moved = moveRight();
  if (e.key === "ArrowUp") moved = moveUp();
  if (e.key === "ArrowDown") moved = moveDown();

  if (moved) {
    addTile();
    render();

    if (isGameOver()) {
      gameOver();
    }
  }
});

/* ======================
   게임 오버 처리
====================== */
function gameOver() {
  gameEnded = true;
  alert("게임 종료! 점수: " + score);
  saveScore(score);
}

/* ======================
   점수 저장 (서버)
====================== */
function saveScore(score) {
  fetch("/game/score", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ score: score })
  })
    .then(res => res.json())
    .then(data => {
      console.log("score saved", data);
    })
    .catch(err => {
      console.error("score save failed", err);
    });
}

/* ======================
   재시작
====================== */
function restartGame() {
  initGame();
}

window.onload = initGame;

