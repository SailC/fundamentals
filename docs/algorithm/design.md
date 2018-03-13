```javascript
// Design and build the board game tic-tac-toe.  Please use real code, no pseudo code please
//   0. Understand the game mechanics: https://upload.wikimedia.org/wikipedia/commons/a/ae/Tic_Tac_Toe.gif
//   1. Pick best data structure to best store a game board
//   2. Write methods for:  setup game, making a move, check winner, error checking
//   3. Game is over when there is a winning hand (3 across, 3 down, or 3 of same diagonally)
class TicTacToe {
    constructor() {
        //player 1 -> +1 , player 2 -> -1
        this.board = new Array(3).fill(0).map(x => new Array(3).fill(0));
        this.cols = new Array(3).fill(0);
        this.rows = new Array(3).fill(0);
        this.diag = 0;
        this.antiDiag = 0;
    }
    // player: Number
    // r: row
    // c: col
    // return: Boolean
    // player1 : -1, player2: 1
    move(player, r, c) {
        if (this.board[r][c] !== 0) return false;
        this.board[r][c] = player;
        this.cols[c] += player;
        this.rows[r] += player;
        const isDiag = (i, j) => i + j === 2;
        const isAntiDiag = (i, j) => i === j;
        if (isDiag(r, c)) this.diag += player;
        if (isAntiDiag(r, c)) this.antiDiag += player;
        return true;
    }

    checkWinner() {
        const PLAYER1 = -1, PLAYER2 = 1;
        for (let row of this.rows) {
            if (row === -3) return PLAYER1;
            if (row === 3) return PLAYER2;
        }
        for (let col of this.cols) {
            if (col === -3) return PLAYER1;
            if (col === 3) return PLAYER2;
        }
        if (this.diag === -3) return PLAYER1;
        if (this.diag === 3) return PLAYER2;
                if (this.antiDiag === -3) return PLAYER1;
        if (this.antiDiag === 3) return PLAYER2;
        return 0;
    }
    print() {
        console.log('board');
        for (let i = 0; i < 3; i++) {
            console.log(this.board[i]);
        }
        console.log('rows');
        console.log(this.rows);

        console.log('cols');
        console.log(this.cols);

        console.log('diag');
        console.log(this.diag);

        console.log('antidiag');
        console.log(this.antiDiag);
    }
}

let ticTacToe = new TicTacToe();
ticTacToe.print();
const PLAYER1 = -1, PLAYER2 = 1;
ticTacToe.move(PLAYER1, 0, 0);
ticTacToe.print();
console.log('winner: ', ticTacToe.checkWinner());
ticTacToe.move(PLAYER1, 0, 1);
ticTacToe.move(PLAYER1, 0, 2);
ticTacToe.print();
console.log('winner: ', ticTacToe.checkWinner());
```
