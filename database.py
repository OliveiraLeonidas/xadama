from shutil import move


class GameState():
    def __init__(self):
        self.board = [
            ["Torre", "Cavalo", "Bispo", "Rei", "Dama", "Bispo", "Cavalo", "Torre"],
            ["Peão", "Peão", "Peão", "Peão", "Peão", "Peão", "Peão", "Peão"],
            ["--", "--", "--", "--", "--", "--", "Checker", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["Checker", "--", "Checker", "--", "Checker", "--", "Checker", "--"],
            ["--", "Checker", "--", "Checker", "--", "Checker", "--", "Checker"],
            ["Checker", "--", "Checker", "--", "Checker", "--", "Checker", "--"]
        ]
        self.moveFunctions = {"Peão": self.getPawnMoves, "Torre": self.getRookMoves, "Checker": self.getCheckerMoves, "Bispo": self.getBishopMoves, "Dama": self.getQueenMoves, "Rei": self.getKingMoves, "Cavalo": self.getKnightMoves}

        self.chessMove = True
        self.moveLog = []

        self.KingLocation = (0, 4)

    def deletePiece(self, r, c):
        self.board[r][c] = "--"

    def createPiece(self, r, c, piece):
        self.board[r][c] = piece

    def makeMove(self, move):
        if move.pieceMoved == "Rei":
            self.KingLocation = (move.endRow, move.endCol)
        if move.pieceMoved != "Checker":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.chessMove = not self.chessMove
            print(move.pieceMoved)
        else:
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.startRow + (move.endRow - move.startRow)/2, move.endCol + (move.endCol - move.startCol)/2] = move.pieceMoved
            #self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            print(move.pieceMoved)
            self.chessMove = not self.chessMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.chessMove = not self.chessMove

            if move.pieceMoved == "Rei":
                self.KingLocation = (move.endRow, move.endCol)

    def getValidMoves(self):
        return self.getAllPossibleMoves()
    

       


    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c]
                if turn != "Checker" and self.chessMove:
                    piece = self.board[r][c]
                    if piece != "--":
                        self.moveFunctions[piece](r, c, moves)

                elif turn == "Checker" and not self.chessMove:
                    self.getCheckerMoves(r, c, moves)


        return moves

    def getCheckerMoves(self, r, c, moves):
        if not self.chessMove:
            if c-1 >= 0:
                if self.board[r-1][c-1] == "--":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                if c-2 >= 0 and self.board[r-2][c-2] == "--" and self.board[r-1][c-1] != "Checker" and self.board[r-1][c-1] != "--":
                    moves.append(Move((r, c), (r-2, c-2), self.board))
                    #self.deletePiece(r-1, c-1)
                    #self.deletePiece(r, c)
                    #self.createPiece(r-2, c-2, "Checker")
                    #self.chessMove = True
            if c+1 <= 7:
                if self.board[r-1][c+1] == "--":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                if c+2 <= 7 and self.board[r-2][c+2] == "--" and self.board[r-1][c+1] != "Checker" and self.board[r-1][c+1] != "--":
                    moves.append(Move((r, c), (r-2, c+2), self.board))
                    #self.deletePiece(r-1, c+1)
                    #self.deletePiece(r, c)
                    #self.createPiece(r-2, c+2, "Checker")
                    #self.chessMove = True   
                    
        else:
            self.chessMove = True
        
                
    def getPawnMoves(self, r, c, moves):
        if self.chessMove:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1] == "Checker":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1] == "Checker":
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    def getKnightMoves(self, r, c, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for i in directions:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0 <= endRow < 8  and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "Checker" or endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        self.verifyAllDirections(directions, moves, r, c)

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        self.verifyAllDirections(directions, moves, r, c)

    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8  and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "Checker" or endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getQueenMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        self.verifyAllDirections(directions, moves, r, c)


    def verifyAllDirections(self, directions, moves, r, c):
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8  and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece == "Checker":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break




class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False



    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
