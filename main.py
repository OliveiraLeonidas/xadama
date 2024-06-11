import pygame
import database

DIMENSION = 8

SIZE = 800

SQ_SIZE = SIZE // DIMENSION

IMAGES = {}

def loadImages():
    pieces = ["Torre", "Cavalo", "Bispo", "Rei", "Dama", "Peão", "Checker"]

    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("imagens/peças/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Xadama")
    clock = pygame.time.Clock()
    screen.fill("white")
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gs = database.GameState()
    validMoves = gs.getValidMoves()

    #loadImages()
    while running:
        validMoves = gs.getValidMoves()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = database.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            #keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)

        clock.tick(60)
        pygame.display.flip()
        
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    screen.blit(pygame.image.load("imagens/background.png"), (0, 0))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE - 3, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                        
if __name__ == "__main__":
    main()

