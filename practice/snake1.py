import pygame
import sys
import random

#define screen
SCREEN_X=1000
SCREEN_Y=600
POINT = 20 #蛇身和食物粒大小

#class snake
#25 pixels every point
class Snake(object):
    def __init__(self):
        self.direction = pygame.K_RIGHT #初始方向向右移动
        self.body = []
        for x in range(5):  #蛇向初始长度为5
            self.addnode()

    #在前端增加一个蛇块
    def addnode(self):
        left,top = (0,0)
        if self.body:
            left,top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left,top,POINT,POINT)
        if self.direction == pygame.K_LEFT:
            node.left -= POINT
        elif self.direction == pygame.K_RIGHT:
            node.left += POINT
        elif self.direction == pygame.K_UP:
            node.top -= POINT
        elif self.direction == pygame.K_DOWN:
            node.top += POINT
        self.body.insert(0,node)

    #删除最后一个蛇块
    def delnode(self):
        self.body.pop()

    #死亡判断
    def isdead(self):
        #撞墙
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True

        #撞自己
        if self.body[0] in self.body[1:]:
            return True
        return False

    #移动
    def move(self):
        self.addnode()
        self.delnode()

    #改变方向，但是左右，上下不能加速或者逆向移动
    def changedirectio(self, curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if curkey in LR+UD:
            if (curkey in LR) and (self.direction in LR):
                return
            if (curkey in UD) and (self.direction in UD):
                return
            self.direction= curkey

#食物类
#方法：放置、移除
class Food(object):
    def __init__(self):
        self.rect = pygame.Rect(-POINT,0,POINT,POINT)

    def remove(self):
        self.rect.x = -POINT

    def set(self):
        if self.rect.x == -POINT:
            allpos_x = []
            allpos_y = []
            #不能靠墙太近，在25-SCREEN_X-25之间
            for pos_x in range(POINT,SCREEN_X-POINT,POINT):
                allpos_x.append(pos_x)
            self.rect.left = random.choice(allpos_x)
            for pos_y in range(POINT,SCREEN_Y-POINT,POINT):
                allpos_y.append(pos_y)
            self.rect.top = random.choice(allpos_y)
            print(self.rect)

def show_text(screen, pos, text, color, font_bold=False, font_size=60, font_italic=False):
    #获取系统字体并设置大小
    cur_font = pygame.font.SysFont("宋体", font_size)
    #设置是否加粗
    cur_font.set_bold(font_bold)
    #设置是否斜体属性
    cur_font.set_italic(font_italic)
    #设置文字内容
    txt_fmt = cur_font.render(text, 1, color)
    #绘制文字
    screen.blit(txt_fmt, pos)

def main():
    pygame.init()
    screen_size = (SCREEN_X,SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    scores = 0
    isdead = False

    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.changedirectio(event.key)
                #死后按空格重新开始
                if event.key == pygame.K_SPACE and isdead:
                    return main()

        screen.fill((255,255,255))

        #画蛇身
        if not isdead:
            snake.move()

        for rect in snake.body:
            pygame.draw.rect(screen, (20,220,39), rect, 0)

        #显示死亡文字
        if snake.isdead():
            show_text(screen,(100,200),"YOU DEAD", (227,29,18),False,100)
            show_text(screen,(150,260), "press space to try again...", (0,0,22),False,40)

        #食物处理，吃掉加10分
        #当食物rect与蛇头重合，吃掉-》Snake增加一个node
        if food.rect == snake.body[0]:
            scores += 10
            food.remove()
            snake.addnode()

        #食物投递
        food.set()
        pygame.draw.rect(screen,(136,0,21),food.rect,0)

        #显示分数
        show_text(screen,(50,500),"Score:"+str(scores), (223,223,223))

        pygame.display.update()
        clock.tick(5) #蛇的移动速度


if __name__ == "__main__":
    main()
