import pygame, sys
from pygame.locals import *

# I have created grid, now i need to track in which grid the bol is


# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 50

# Global Variables to be used through our program

WINDOWWIDTH = 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
startCount = False

# Set up the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
count = 0
image = 0
track = False
foundInCell = 1000
foundInCellY = 1000
ballX_old = 0
ballY_old = 0
global listArr
listArr=[]

def addToList(item):
    listArr.append(item)

def getListSet(listArr):
    listTemp=list(set(listArr))
    listArr=[]
    return listTemp

# Draws the arena the game will be played in.
def drawArena():
    DISPLAYSURF.fill((0, 0, 0))
    # Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS * 2)
    # Draw centre line
    # pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), (LINETHICKNESS/4))
    for num in range(LINETHICKNESS, 380, 38):
        pygame.draw.line(DISPLAYSURF, WHITE, (num, 0), (num, WINDOWHEIGHT), (LINETHICKNESS / 4))
    for num in range(LINETHICKNESS, 280, 28):
        pygame.draw.line(DISPLAYSURF, WHITE, (0, num), (WINDOWWIDTH, num), (LINETHICKNESS / 4))


def getPaddleXY(paddle2):
    paddle2X = paddle2.top
    paddle2Y = paddle2.bottom
    print ' Hit at location ', paddle2X, paddle2Y
    # render text
    label = BASICFONT.render(str(paddle2X / 38) + str(paddle2Y / 28), 1, (255, 99, 71))
    DISPLAYSURF.blit(label, (paddle2X/38, paddle2Y/28))
    return paddle2X,paddle2Y

# Function to track ball is in which grid cell
def trackBall(ball):
    cell = 0
    celly = 0
    global foundInCell, foundInCellY
    if foundInCell != cell:
        for x0 in range(LINETHICKNESS, 380, 38):
            x1 = x0 + 38
            cell += 1
            if (ball.x + LINETHICKNESS) in range(x0, x1):
                # print 'Found in cell ', cell
                break

    if foundInCellY != celly:
        for y0 in range(LINETHICKNESS, 280, 28):
            y1 = y0 + 28
            celly += 1
            if (ball.y + LINETHICKNESS) in range(y0, y1):
                break
    # render text
    label = myfont.render(str(cell) + str(celly), 1, (255, 255, 0))
    listArr.append(str(cell) + str(celly)) # add the elements to the list
    DISPLAYSURF.blit(label, (cell * 36, celly * 26))
    # getPaddleXY(paddle2)
    # print 'X,Y ', cell, celly


def displayMessage(startCount):
    if (startCount == True):
        print 'Starting count'
    else:
        print 'Stopping Count'


def setStartCount(value):
    global startCount
    startCount = value


# Draws the paddle
def drawPaddle(paddle):
    # Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    # Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)


# draws the ball
def drawBall(ball, ballDirX, ballDirY, paddle2):
    global ballX_old, foundInCell, foundInCellY, ballY_old
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)
    trackBall(ball)
    if ballDirX == -1:  # left
        if ballX_old not in range(ball.x, ball.x + 38):
            ballX_old = ball.x
            if ballY_old not in range(ball.y, ball.y + 28):
                ballY_old = ball.y
                trackBall(ball)
    else:
        if ballX_old not in range(ball.x - 38, ball.x):
            ballX_old = ball.x
            if ballY_old not in range(ball.y - 28, ball.y):
                ballY_old = ball.y
                trackBall(ball)


# moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball


# Checks for a collision with a wall, and 'bounces' ball off it.
# Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1  # ball hit the top and bottom walls
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1  # ball hit the left or right walls
    return ballDirX, ballDirY


# Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        # positive value expereince
        global count
        count = 0
        startCount = False
        displayMessage(startCount)
        setStartCount(startCount)
        print 'Stopped Collecting Values'
        print getListSet(listArr)

        return -1  # ball hit the paddle 1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        # start recording the value of X
        print 'Start Collecting Values'
        global count
        count = 0
        startCount = True
        getPaddleXY(paddle2)
        displayMessage(startCount)
        setStartCount(startCount)
        return -1  # ball hit the paddle 2
    else:
        return 1


# Checks to see if a point has been scored returns new score
def checkPointScored(paddle1, ball, score, ballDirX):
    # reset points if left wall is hit
    if ball.left == LINETHICKNESS:
        # this will be loosing move
        return 0
    # 1 point for hitting the ball
    elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        # this will be winning move
        return score
    # 5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score
    # if no points scored, return score unchanged
    else:
        return score


# Artificial Intelligence of computer player
def artificialIntelligence(ball, ballDirX, paddle2):
    # If ball is moving away from paddle, center bat
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT / 2):
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT / 2):
            paddle2.y -= 1
    # if ball moving towards bat, track its movement.
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2


# Displays the current score on the screen
def displayScore(score):
    resultSurf = BASICFONT.render('Score = %s' % (score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)


# Main function
def main():
    pygame.init()
    global myfont
    global DISPLAYSURF
    myfont = pygame.font.SysFont("monospace", 15)
    ##Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pong')

    # Initiate variable and set starting positions
    # any future changes made within rectangles
    ballX = WINDOWWIDTH / 2 - LINETHICKNESS / 2
    ballY = WINDOWHEIGHT / 2 - LINETHICKNESS / 2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    score = 0

    # Keeps track of ball direction
    ballDirX = -1  ## -1 = left 1 = right
    ballDirY = -1  ## -1 = up 1 = down

    # Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    # Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball, ballDirX, ballDirY, paddle2)
    pygame.mouse.set_visible(0)  # make cursor invisible

    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball, ballDirX, ballDirY, paddle2)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(paddle1, ball, score, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = artificialIntelligence(ball, ballDirX, paddle2)

        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
