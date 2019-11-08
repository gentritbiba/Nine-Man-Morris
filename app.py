import pygame
import time

pygame.init()
screenWidh=1000
screenHeight=1000
boardSize=600
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)


screen = pygame.display.set_mode((screenWidh, screenHeight))

pygame.display.set_caption("NMM")
background = pygame.image

class Point:
   def __init__(self,owns,posX,posY):
       self.owns = owns
       self.X = posX
       self.Y = posY

class Board:
    def __init__(self):
        self.cleanBoard()
    points=[]
    def cleanBoard(self):
        self.points=[]
        self.phaseOneCountDown=7
        outerLine,midLine,innerLine=[],[],[]
        for i in range(8):
            if i < 3:
                outerLine.append(Point(None, i*boardSize/2, 0))
                midLine.append(Point(None, boardSize/6 + i*boardSize/3, boardSize/6))
                innerLine.append(Point(None, boardSize/3 + i*boardSize/6, boardSize/3))
            elif i < 5:
                outerLine.append(Point(None, boardSize,(i-2)*boardSize/2))
                midLine.append(Point(None, boardSize - boardSize/6, boardSize/6 + (i-2)*boardSize/3))
                innerLine.append(Point(None, boardSize - boardSize/3, boardSize/3 + (i-2)*boardSize/6))
            elif i < 7:
                outerLine.append(Point(None, (6-i)*boardSize/2, boardSize))
                midLine.append(Point(None, boardSize/6 + (6-i)*boardSize/3, boardSize - boardSize/6))
                innerLine.append(Point(None, boardSize/3 + (6-i)*boardSize/6, boardSize - boardSize/3))
            else:
                outerLine.append(Point(None, 0, boardSize/2))
                midLine.append(Point(None, boardSize/6, boardSize/2))
                innerLine.append(Point(None, boardSize/3, boardSize/2))
        self.points.extend([outerLine,midLine,innerLine])

    def possibleMoves(self,point):
        boardIndex=-1
        lineIndex=-1
        for index,subArr in enumerate(self.points):
            try:
                lineIndex=subArr.index(point)
                boardIndex=index
                break
            except:
                continue
        possibleMoves = []
        try:
            if self.points[boardIndex+1][lineIndex].owns == None and boardIndex !=2 and lineIndex % 2 == 1:
                possibleMoves.append(self.points[boardIndex+1][lineIndex])
        except IndexError:
            pass
        try:
            if self.points[boardIndex-1][lineIndex].owns == None and boardIndex !=0 and lineIndex % 2 == 1:
                possibleMoves.append(self.points[boardIndex-1][lineIndex])
        except IndexError:
            pass
        try:
            if lineIndex != 7 and self.points[boardIndex][lineIndex+1].owns == None:
                possibleMoves.append(self.points[boardIndex][lineIndex+1])
            elif self.points[boardIndex][0].owns == None and lineIndex == 7:
                possibleMoves.append(self.points[boardIndex][0])
        except IndexError:
            pass
        try:
            if self.points[boardIndex][lineIndex-1].owns == None:
                if lineIndex == 0:
                    possibleMoves.append(self.points[boardIndex][7])
                else:
                    possibleMoves.append(self.points[boardIndex][lineIndex-1])

        except IndexError:
            pass
        return possibleMoves

    def freePoints(self):
        returnThis=[]
        for i in self.points:
            for point in i:
                if point.owns==None:
                    returnThis.append(point)
        return returnThis
    
    def playerPointsLen(self,playerTurn):
        returnThis=[]
        for i in self.points:
            for point in i:
                if point.owns==playerTurn:
                    returnThis.append(point)
        return len(returnThis)

    def end_if_no_moves(self,playerTurn):
        freeMoves=0
        for i in self.points:
            for point in i:
                if point.owns==playerTurn:
                    freeMoves+= len(self.possibleMoves(point))
        if freeMoves==0 and not self.phaseOneCountDown:
            print("Player %s has lost by having no more possible moves" % playerTurn)
            time.sleep(0.4)
            self.cleanBoard()
            playerTurn=1
        return playerTurn
    def isMill(self,point):
        boardIndex=-1
        lineIndex=-1
        for index,subArr in enumerate(self.points):
            try:
                lineIndex=subArr.index(point)
                boardIndex=index
                break
            except:
                continue
            if lineindex % 2 == 1:
                if self.points[0][lineIndex].owns == point.owns and self.points[1][lineIndex].owns == point.owns and self.points[2][lineIndex].owns == point.owns:
                    return True
            # for i in range(3
            


            


                 


running = True

board = Board()

# print(board.points[1][7].X,board.points[1][7].Y)
clock = pygame.time.Clock()
FPS= 20
playerTurn=1
focus=0
moves=[]
# GAME LOOP
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        playerTurn = board.end_if_no_moves(playerTurn)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mX,mY = pygame.mouse.get_pos()
            if focus:
                for point in moves:
                    if abs(mX - point.X - (screenWidh-boardSize)/2)<=20 and abs(mY-(screenWidh-boardSize)/2 - point.Y)<=20:
                        try:
                            focus.owns=None
                            point.owns=playerTurn
                            playerTurn = playerTurn % 2 + 1
                            focus = 0
                            moves = []
                        except:
                            pass

            for posBoard,i in enumerate(board.points):
                for point in i:
                    # print(abs(mX-point.X),mX,mY)
                    if abs(mX - point.X - (screenWidh-boardSize)/2)<=20 and abs(mY-(screenWidh-boardSize)/2 - point.Y)<=20:
                        if board.phaseOneCountDown and not point.owns:
                            posLine=i.index(point)
                            point.owns = playerTurn
                            playerTurn = playerTurn % 2 + 1
                            # print(point.owns,i.index(point),posBoard,board.possibleMoves(point))
                            board.phaseOneCountDown-=1
                        elif not board.phaseOneCountDown and point.owns == playerTurn:
                            focus = point
                            moves = board.possibleMoves(focus) if board.playerPointsLen(playerTurn) != 3 else board.freePoints()
                            print('-----')
                            for i in moves:
                                print(i.X,i.Y)
            
                    
                            
                            
            
    screen.fill((255, 255, 255))
    # pygame.draw.circle(screen, BLACK, (100, 100), 100 ,1)
    #pygame.draw.line(screen, BLACK, ((screenWidh-boardSize)/2, screenWidh/2), ((screenHeight-boardSize)/2, screenHeight/2))
    pygame.draw.line(screen, BLACK, (screenWidh/2, (screenWidh-boardSize)/2), (screenWidh/2, screenHeight-(screenHeight-boardSize)/2))
    pygame.draw.line(screen, BLACK, ((screenHeight-boardSize)/2, screenHeight/2), (screenWidh-(screenWidh-boardSize)/2, screenHeight/2))

    pygame.draw.rect(screen, BLACK, ((screenWidh-boardSize)/2, (screenHeight-boardSize)/2, boardSize, boardSize), 1)
    pygame.draw.rect(screen, BLACK, ((screenWidh-boardSize*2/3)/2, (screenHeight-boardSize*2/3)/2, boardSize*2/3, boardSize*2/3), 1)
    pygame.draw.rect(screen, BLACK, ((screenWidh-boardSize/3)/2, (screenHeight-boardSize/3)/2, boardSize/3, boardSize/3))
    pygame.draw.rect(screen, (255, 255, 255), ((screenWidh-boardSize/3)/2+1, (screenHeight-boardSize/3)/2+1, boardSize/3-2, boardSize/3-2))
    # for i in board.points:
    #     for j in i:
    #         pygame.draw.circle(screen, BLACK, ((screen-boardSize)/2 + j['posX'] ,(screen-boardSize)/2 + j['posy'] ), 5 ,1)
    for i in board.points:
        for point in i:
            if not point.owns:
                pygame.draw.circle(screen, GRAY, (int((screenWidh-boardSize)/2 + point.X) ,int((screenHeight-boardSize)/2 + point.Y) ), 4 + 4 * ([point.X,point.Y] in moves))
            elif point.owns == 1:
                pygame.draw.circle(screen, BLACK, (int((screenWidh-boardSize)/2 + point.X) ,int((screenHeight-boardSize)/2 + point.Y) ), 20 + 10 * (focus and point == focus))
            elif point.owns == 2:
                pygame.draw.circle(screen, RED, (int((screenWidh-boardSize)/2 + point.X) ,int((screenHeight-boardSize)/2 + point.Y) ), 20 + 10 * (focus and point == focus))
                


    pygame.display.update()

