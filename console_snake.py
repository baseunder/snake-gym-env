import numpy as np
import os
import sys
import random

def moveCursor(y, x):
    print("\033[%d;%dH" % (y, x))

class ConsoleSnake:
    def __init__(self, fieldsize=7, maxround=1000):
        self.FIELD = fieldsize
        self.MAXROUND = maxround
        self.reset()
        os.system("clear")

    def reset(self):
        self.food = np.zeros((self.FIELD,self.FIELD),dtype='float32')
        self.head = np.zeros((self.FIELD,self.FIELD),dtype='float32')
        self.body = np.zeros((self.FIELD,self.FIELD),dtype='float32')
        self.setHead()
        self.setFood()
        self.ROUNDSTEP = 0
        return np.dstack([self.food, self.head, self.body])

    def setFood(self):
        ps = np.transpose(np.where(self.body==0))
        while True:
            p,s = random.choice(ps)
            if not self.head[p,s]:
                self.food[p,s] = True
                break
    def setHead(self):
        ps = np.transpose(np.where(self.head==0))
        p,s = random.choice(ps)
        self.head[p,s] = True

    def step(self,d):
        done = False
        self.ROUNDSTEP += 1
        if self.ROUNDSTEP > self.MAXROUND:
            done = True
        reward = -1
        y, x = np.where(self.head)
        oy, ox = np.where(self.head)
        self.head[y,x] = False
        if d==0:
            y -= 1
        elif d==1:
            x -= 1
        elif d==2:
            y += 1
        elif d==3:
            x += 1
        if y < 0 or y == self.FIELD:
            #print("y crash")
            done = True
            reward -= 50
        elif x < 0 or x == self.FIELD:
            #print("x crash")
            done = True
            reward -= 50
        if not done:
            self.head[y,x] = True
            self.body[oy,ox] = np.max(self.body)+1
            if self.food[y,x]:
                self.food[y,x] = False
                self.setFood()
                reward += 20
            else:
                for q, w in np.transpose(np.where(self.body)):
                    self.body[q,w] -= 1
            if np.any(self.head * self.body):
                #print("head an body collide")
                done = True
                reward -= 50
        return np.dstack([self.food, self.head, self.body]), reward, done, None

    def render(self):
        moveCursor(0,0)
        print(" "+"".join(["-" for _ in range(self.FIELD)]))
        white = " "
        for y in range(self.FIELD):
            print("|",end='')
            for x in range(self.FIELD):
                if self.body[y,x] or self.head[y,x] or self.food[y,x]:
                    if self.body[y,x]:
                        print('o',end='')
                    elif self.head[y,x]:
                        print("@",end='')
                    elif self.food[y,x]:
                        print("X",end='')
                else:
                    print(white,end='')
            print("|")
        print(" "+"".join(["-" for _ in range(self.FIELD)]))
        print()

def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getwch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return ord(result)

def randomAction():
    return random.randint(0,3)

if __name__ == "__main__":
    snake = ConsoleSnake(13)
    while True:
        snake.render()
        k = wait_key()-105
        state, reward, done, _ = snake.step(k)
        if done:
            print("game over")
            snake.reset()