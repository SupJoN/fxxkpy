# coding:utf-8
# 飞机大战
def AircraftWar():
    # 导入模块
    import os
    import random
    import time
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ''  # 隐藏pygame的import欢迎显示
    import pygame

    # 初始化pygame环境
    pygame.init()

    # 创建一个长宽分别为1200/715的白色窗口
    x = 80
    y = 27
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    canvas = pygame.display.set_mode((1200, 715))
    canvas.fill((255, 255, 255))

    # 设置窗口标题
    pygame.display.set_caption("飞机大战")

    # 敌飞机图片数组
    file = os.path.split(os.path.abspath(__file__))[0]
    e1 = []
    e1.append(pygame.image.load(file + "/game/AircraftWar/enemy1.png"))
    e1.append(pygame.image.load(file + "/game/AircraftWar/enemy1_down1.png"))
    e1.append(pygame.image.load(file + "/game/AircraftWar/enemy1_down2.png"))
    e1.append(pygame.image.load(file + "/game/AircraftWar/enemy1_down3.png"))
    e1.append(pygame.image.load(file + "/game/AircraftWar/enemy1_down4.png"))
    e1.append(pygame.image.load(file + "/game/AircraftWar/enemy1_down5.png"))
    e2 = []
    e2.append(pygame.image.load(file + "/game/AircraftWar/enemy2.png"))
    e2.append(pygame.image.load(file + "/game/AircraftWar/enemy2_down1.png"))
    e2.append(pygame.image.load(file + "/game/AircraftWar/enemy2_down2.png"))
    e2.append(pygame.image.load(file + "/game/AircraftWar/enemy2_down3.png"))
    e2.append(pygame.image.load(file + "/game/AircraftWar/enemy2_down4.png"))
    e2.append(pygame.image.load(file + "/game/AircraftWar/enemy2_down5.png"))
    e3 = []
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_1.png"))
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_2.png"))
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_down1.png"))
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_down2.png"))
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_down3.png"))
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_down4.png"))
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_down5.png"))
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_down6.png"))
    e3.append(pygame.image.load(file + "/game/AircraftWar/enemy3_down7.png"))
    # 英雄机图片数组
    h = []
    h.append(pygame.image.load(file + "/game/AircraftWar/hero.png"))
    h.append(pygame.image.load(file + "/game/AircraftWar/hero_down1.png"))
    h.append(pygame.image.load(file + "/game/AircraftWar/hero_down2.png"))
    h.append(pygame.image.load(file + "/game/AircraftWar/hero_down3.png"))
    h.append(pygame.image.load(file + "/game/AircraftWar/hero_down4.png"))
    # 背景图片
    bg = pygame.image.load(file + "/game/AircraftWar/bg.jpg")
    # 子弹图片
    b = []
    b.append(pygame.image.load(file + "/game/AircraftWar/bullet.png"))
    # 开始游戏图片
    startgame = pygame.image.load(file + "/game/AircraftWar/startGame.png")
    # logo图片
    logo = pygame.image.load(file + "/game/AircraftWar/LOGO.png")
    # 暂停图片
    pause = pygame.image.load(file + "/game/AircraftWar/game_pause_nor.png")
    score = pygame.image.load(file + "/game/AircraftWar/score.png")
    over = pygame.image.load(file + "/game/AircraftWar/over.png")

    # 键盘事件检测
    def handleEvent():
        for event in pygame.event.get():
            event: pygame.event.Event
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return True
            # 监听鼠标移动事件
            if event.type == pygame.MOUSEMOTION:
                # 根据鼠标的坐标修改英雄机的坐标
                # 使用get_width函数可以获取图片的宽度
                if GameVar.state == GameVar.STATES["RUNNING"]:
                    GameVar.hero.x = event.pos[0] - GameVar.hero.width / 2
                    GameVar.hero.y = event.pos[1] - GameVar.hero.height / 2
                # 鼠标移入移出事件切换状态
                if isMouseOut(event.pos[0], event.pos[1]):
                    if GameVar.state == GameVar.STATES["RUNNING"]:
                        GameVar.state = GameVar.STATES["PAUSE"]
                if isMouseOver(event.pos[0], event.pos[1]):
                    if GameVar.state == GameVar.STATES["PAUSE"]:
                        GameVar.state = GameVar.STATES["RUNNING"]

            # 点击左键切换为运行状态
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if GameVar.state == GameVar.STATES["START"]:
                    GameVar.state = GameVar.STATES["RUNNING"]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if GameVar.state == GameVar.STATES["GAME_OVER"]:
                    GameVar.score = 0
                    GameVar.heroes = 4
                    GameVar.state = GameVar.STATES["START"]

    # 画图
    def draw(img, x, y):
        canvas.blit(img, (x, y))

    # 工具方法-判断时间间隔是否到了
    def isActionTime(lastTime, interval):
        if lastTime == 0:
            return True
        currentTime = time.time()
        return currentTime - lastTime >= interval

    # 工具方法-写文字方法
    def renderText(text, position, view=canvas):
        # 设置字体样式和大小
        font = pygame.font.Font(file + "/game/AircraftWar/font.ttf", 30)
        # 渲染文字
        text = font.render(text, True, (255, 255, 255))
        view.blit(text, position)

    # 工具方法-判断鼠标是否移出了游戏区域
    def isMouseOut(x, y):
        if x >= 1190 or x <= 0 or y > 700 or y <= 0:
            return True
        else:
            return False

    # 工具方法-判断鼠标是否移入了游戏区域
    def isMouseOver(x, y):
        if x > 0 and x < 1150 and y > 1 and y < 648:
            return True
        else:
            return False

    # 定义Sky类
    class Sky(object):
        def __init__(self):
            self.width = 480
            self.height = 680
            self.img = bg
            self.x1 = 0
            self.y1 = 0
            self.x2 = 0
            self.y2 = -self.height

        def paint(self, view):
            draw(self.img, self.x1, self.y1)
            draw(self.img, self.x2, self.y2)

        def step(self):
            self.y1 = self.y1 + 1
            self.y2 = self.y2 + 1
            if self.y1 > self.height:
                self.y1 = -self.height
            if self.y2 > self.height:
                self.y2 = -self.height

    # 定义父类FlyingObject
    class FlyingObject(object):
        def __init__(self, x, y, width, height, life, frames, baseFrameCount):
            self.x = x
            self.y = y
            self.score = 0
            self.width = width
            self.height = height
            self.life = life
            # 敌飞机移动的时间间隔
            self.lastTime = 0
            self.interval = 0.01
            # 添加掉落属性和删除属性
            self.down = False
            self.canDelete = False
            # 实现动画所需属性
            self.frames = frames
            self.frameIndex = 0
            self.img = self.frames[self.frameIndex]
            self.frameCount = baseFrameCount

        # 画图方法
        def paint(self, view):
            draw(self.img, self.x, self.y)

        # 移动方法
        def step(self):
            # 判断是否到了移动的时间间隔
            if not isActionTime(self.lastTime, self.interval):
                return
            self.lastTime = time.time()
            # 控制移动速度
            self.y = self.y + 5

        # 碰撞检测方法
        def hit(self, component: "FlyingObject"):
            return component.x > self.x - component.width and component.x < self.x + self.width and component.y > self.y - component.height and component.y < self.y + self.height

        # 处理碰撞发生后要做的事
        def bang(self):
            self.life -= 1
            if self.life == 0:
                # 生命值为0时将down置为True
                self.down = True
                # 将frameIndex切换为销毁动画的第一张
                self.frameIndex = self.frameCount

                if hasattr(self, "score"):
                    GameVar.score += self.score

        # 越界处理
        def outOfBounds(self):
            return self.y > 650

        # 实现动画
        def animation(self):
            if self.down:
                # 销毁动画播放完后将canDelete置为True
                if self.frameIndex == len(self.frames):
                    self.canDelete = True
                else:
                    self.img = self.frames[self.frameIndex]
                    self.frameIndex += 1
            else:
                self.img = self.frames[self.frameIndex % self.frameCount]
                self.frameIndex += 1

    # 定义Enemy类
    class Enemy(FlyingObject):
        def __init__(self, x, y, width, height, type, life, score, frames, baseFrameCount):
            FlyingObject.__init__(self, x, y, width, height,
                                  life, frames, baseFrameCount)
            self.x = random.randint(0, 1300 - self.width)
            self.y = -self.height
            self.type = type
            self.score = score

    # 定义Hero类
    class Hero(FlyingObject):
        def __init__(self, x, y, width, height, life, frames, baseFrameCount):
            FlyingObject.__init__(self, x, y, width, height,
                                  life, frames, baseFrameCount)
            self.width = 60
            self.height = 75
            self.x = 450 + 480 / 2 - self.width / 2
            self.y = 650 - self.height - 30

        def paint(self, view):
            draw(self.img, self.x, self.y)

        def shoot(self):
            GameVar.bullets.append(
                Bullet(self.x + self.width / 2 - 20, self.y, 9, 21, 1, b, 1))
            GameVar.bullets.append(
                Bullet(self.x + self.width / 2 + 10, self.y, 9, 21, 1, b, 1))

    # 定义Bullet类
    class Bullet(FlyingObject):
        def __init__(self, x, y, width, height, life, frames, baseFrameCount):
            FlyingObject.__init__(self, x, y, width, height,
                                  life, frames, baseFrameCount)

        # 重写step方法
        def step(self):
            self.y = self.y - 10

        # 重写判断是否越界的方法
        def outOfBounds(self):
            return self.y < -self.height

    # 生成组件
    def componentEnter():
        # 判断是否到了产生敌飞机的时间
        if not isActionTime(GameVar.lastTime, GameVar.interval):
            return
        GameVar.lastTime = time.time()

        # 随机生成坐标
        _x = 40
        x1 = random.randint(_x, 1200 - 57 - _x)
        x2 = random.randint(_x, 1200 - 50 - _x)
        x3 = random.randint(_x, 1200 - 169 - _x)
        # 根据随机整数的值生成不同的敌飞机
        n = random.randint(0, 9)
        if n <= 7:
            # 因为列表初始值为空，所以这里可以使用append或insert进行添加元素，append会将新增的追加到末尾，但insert会将新增的插入到指定位置
            GameVar.enemies.append(Enemy(x1, -45, 57, 45, 1, 1, 1, e1, 1))
        elif n == 8:
            GameVar.enemies.append(Enemy(x2, -68, 50, 68, 2, 3, 5, e2, 1))
        elif n == 9:
            # 将打飞机放在列表中索引为0的位置
            if len(GameVar.enemies) == 0 or GameVar.enemies[0].type != 3:
                GameVar.enemies.insert(
                    0, Enemy(x3, -258, 169, 258, 3, 10, 20, e3, 2))

    # 画组件方法
    def paintComponent(view):
        # 判断是否到了飞行物重绘的时间
        if not isActionTime(GameVar.paintLastTime, GameVar.paintInterval):
            return
        GameVar.paintLastTime = time.time()

        # 调用sky对象的paint方法
        GameVar.sky.paint(view)
        # 画敌飞机并实现敌飞机移动
        for enemy in GameVar.enemies:
            enemy: Enemy
            enemy.paint(view)
        # 画英雄机
        GameVar.hero.paint(view)
        # 画子弹
        for bullet in GameVar.bullets:
            bullet: Bullet
            bullet.paint(view)
        # 写分数和生命值
        draw(score, 720 + 210, 10)
        renderText(str(GameVar.score), (780 + 305, 25))
        renderText(str(GameVar.heroes), (780 + 305, 58))

    # 组件移动方法
    def componentStep():
        # 调用sky对象的step方法
        GameVar.sky.step()
        # 调用enemy对象的step方法
        for enemy in GameVar.enemies:
            enemy: Enemy
            enemy.step()
        # 调用bullet对象的step方法
        for bullet in GameVar.bullets:
            bullet: Bullet
            bullet.step()

    # 检测组件碰撞
    def checkHit():
        # 判断敌飞机是否和英雄机相撞
        for enemy in GameVar.enemies:
            enemy: Enemy
            # 如果当前飞机已经死亡则换下一架飞机
            if enemy.down == True:
                continue

            if GameVar.hero.hit(enemy):
                enemy.bang()
                GameVar.hero.bang()
            for bullet in GameVar.bullets:
                bullet: Bullet
                # 如果当前子弹是无效的子弹则换下一颗子弹
                if bullet.down == True:
                    continue

                if enemy.hit(bullet):
                    enemy.bang()
                    bullet.bang()

    # 删除无效组件
    def deleteComponent():
        # 删除无效的敌飞机
        for i in range(len(GameVar.enemies) - 1, -1, -1):
            enemy: Enemy = GameVar.enemies[i]
            if enemy.canDelete or enemy.outOfBounds():
                GameVar.enemies.remove(enemy)
        # 删除无效子弹
        for i in range(len(GameVar.bullets) - 1, -1, -1):
            bullet: Bullet = GameVar.bullets[i]
            if bullet.canDelete or bullet.outOfBounds():
                GameVar.bullets.remove(bullet)
        # 删除无效的英雄机
        if GameVar.hero.canDelete == True:
            GameVar.heroes -= 1
            if GameVar.heroes == 0:
                GameVar.state = GameVar.STATES["GAME_OVER"]
            else:
                GameVar.hero = Hero(0, 0, 60, 75, 1, h, 1)

    # 组件的动画
    def componentAnimation():
        # 敌飞机播放动画
        for enemy in GameVar.enemies:
            enemy: Enemy
            enemy.animation()
        # 子弹播放动画
        for bullet in GameVar.bullets:
            bullet: Bullet
            bullet.animation()
        # 英雄机播放动画
        GameVar.hero.animation()

    # 使用类属性存储游戏中的变量，以减少全局变量的数量
    class GameVar(object):
        sky = None
        # 英雄机对象
        hero: Hero = Hero(0, 0, 60, 75, 1, h, 1)
        # 敌机对象列表
        enemies = []
        # 天空背景对象
        sky: Sky = Sky()
        # 子弹列表
        bullets = []

        # 产生敌飞机的时间间隔
        lastTime = 0
        interval = 0.5  # 单位为秒
        # 重绘飞行物的时间间隔
        paintLastTime = 0
        paintInterval = 0.03
        # 分数和生命值
        score = 0
        heroes = 5
        # 控制游戏状态
        STATES = {"START": 1, "RUNNING": 2, "PAUSE": 3, "GAME_OVER": 4}
        state = STATES["START"]

    # 游戏状态控制
    def contralState():
        if GameVar.state == GameVar.STATES["START"]:
            GameVar.sky.paint(canvas)
            GameVar.sky.step()
            draw(logo, 200, 200)
            draw(startgame, 460, 450)
        elif GameVar.state == GameVar.STATES["RUNNING"]:
            componentEnter()
            # 画组件
            paintComponent(canvas)
            # 组件移动
            componentStep()
            # 播放组件动画
            componentAnimation()
            # 英雄机发射子弹
            GameVar.hero.shoot()
            # 碰撞检测
            checkHit()
            # 删除无效组件
            deleteComponent()
        elif GameVar.state == GameVar.STATES["PAUSE"]:
            paintComponent(canvas)
            GameVar.sky.step()
            draw(pause, 500, 250)
        elif GameVar.state == GameVar.STATES["GAME_OVER"]:
            paintComponent(canvas)
            GameVar.sky.step()
            draw(over, 230, 250)

    while True:
        # 监听有没有按下退出按钮
        if handleEvent():
            break
        # 游戏状态控制
        contralState()
        # 更新屏幕内容
        pygame.display.update()
        # 等待0.01秒后再进行下一次循环
        pygame.time.delay(15)


# 红心大战
def HeartWar():
    import os
    import random
    import time
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ''  # 隐藏pygame的import欢迎显示
    import pygame

    # 初始化pygame环境
    pygame.init()

    # 创建一个长宽分别为480/650的窗口
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 50)
    canvas = pygame.display.set_mode((480, 650))

    # 设置窗口标题
    pygame.display.set_caption("红心大战")

    # 加载图片
    file = os.path.split(os.path.abspath(__file__))[0]
    bg1 = pygame.image.load(file + "/game/HeartWar/bg1.png")
    bg2 = pygame.image.load(file + "/game/HeartWar/bg2.png")
    bg3 = pygame.image.load(file + "/game/HeartWar/bg3.png")
    loveR = pygame.image.load(file + "/game/HeartWar/loveRed.png")
    loveB = pygame.image.load(file + "/game/HeartWar/loveBlack.png")

    # 退出和加生命方法
    key = {"p": 0, "l": 0, "u": 0, "s": 0}

    def handleEvent():
        for event in pygame.event.get():
            event: pygame.event.Event
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    key["p"] = time.time()
                if event.key == pygame.K_p:
                    key["l"] = time.time()
                if event.key == pygame.K_p:
                    key["u"] = time.time()
                if event.key == pygame.K_p:
                    key["s"] = time.time()
                if event.key == pygame.K_0:
                    rlove.life += 1
        if key["p"] < key["l"] < key["u"] < key["s"] and \
                key["l"] - key["p"] <= 1 and \
                key["u"] - key["l"] <= 1 and \
                key["s"] - key["u"] <= 1:
            rlove.life += 1

    # 写文字方法
    def fillText(text, position):
        TextFont = pygame.font.Font(file + "/game/HeartWar/font.ttf", 25)
        newText = TextFont.render(text, True, (255, 0, 0))
        canvas.blit(newText, position)

    # 声明变量life表示红心的生命值
    life = 5

    # 保存黑心变量
    mouseX = 200
    mouseY = 200
    bWidth = 18
    bHeight = 18
    bSpeed = 210

    # 创建黑心方法
    arrBlove = []

    def createBlove(bloveNum):
        for i in range(0, bloveNum):
            randPos = random.randint(0, 3)
            randX = random.random()*(480 - bWidth)
            randY = random.random()*(480 - bHeight)
            speed = random.random()*200 + bSpeed
            if randPos == 0:
                arrBlove.append(Blove(randX, 0, loveB, bWidth,
                                      bHeight, mouseX, mouseY, speed))
            elif randPos == 1:
                arrBlove.append(Blove(462, randY, loveB, bWidth,
                                      bHeight, mouseX, mouseY, speed))
            elif randPos == 2:
                arrBlove.append(Blove(randX, 632, loveB, bWidth,
                                      bHeight, mouseX, mouseY, speed))
            elif randPos == 3:
                arrBlove.append(Blove(0, randY, loveB, bWidth,
                                      bHeight, mouseX, mouseY, speed))

    # 创建黑心类
    class Blove():
        nonlocal mouseX, mouseY

        def __init__(self, x, y, img, width, height, mouseX, mouseY, speed):
            self.x = x
            self.y = y
            self.img = img
            self.width = width
            self.height = height
            self.mouseX = mouseX
            self.mouseY = mouseY
            self.speed = speed
            self.xs = (self.mouseX - self.x) / speed
            self.ys = (self.mouseY - self.y) / speed

    # 创建红心类
    class Rlove(Blove):
        nonlocal mouseX, mouseY, life

        def __init__(self, x, y, img, width, height, mouseX, mouseY, speed, life, invincible_time):
            Blove.__init__(self, x, y, img, width,
                           height, mouseX, mouseY, speed)
            self.life = life
            self.invincible_time = invincible_time

    # 创建红心对象
    start = time.time()
    rlove = Rlove(mouseX, mouseY, loveR, 45, 25, 0, 0, 1, life, start)

    # 创建生成黑心对象方法
    bloveNum = 0

    def born():
        nonlocal bloveNum
        if len(arrBlove) <= 0:
            bloveNum = bloveNum + 1
            createBlove(bloveNum)

    # 创建画图片方法
    def drawAll():
        canvas.blit(bg2, (0, 0))
        # 绘制黑心
        for arrB in arrBlove:
            arrB: Blove
            canvas.blit(arrB.img, (arrB.x, arrB.y))
        # 绘制红心图片
        canvas.blit(rlove.img, (rlove.x, rlove.y))

    # 创建移动方法
    def moveAll():
        nonlocal mouseX, mouseY
        for arrB in arrBlove:
            arrB: Blove
            arrB.x = arrB.xs + arrB.x
            arrB.y = arrB.ys + arrB.y
        # 设置红心跟随鼠标移动
        mouseX, mouseY = pygame.mouse.get_pos()
        rlove.x = mouseX - rlove.width / 2
        rlove.y = mouseY - rlove.height / 2

    # 创建越界检测方法
    def outSide():
        for arrB in arrBlove:
            arrB: Blove
            if arrB.x + arrB.width < 0 or arrB.x > 480 or arrB.y + arrB.height < 0 or arrB.y > 650:
                arrBlove.remove(arrB)
            break

    # 创建碰撞检测方法
    def collision():
        for arrB in arrBlove:
            arrB: Blove
            if arrB.x + arrB.width > rlove.x and arrB.x < rlove.x + rlove.width:
                if arrB.y + arrB.height > rlove.y and arrB.y < rlove.y + rlove.height:
                    if time.time() - rlove.invincible_time > 1:
                        rlove.life -= 1
                        rlove.invincible_time = time.time()
                        if rlove.life == 0:
                            canvas.blit(bg1, (0, 0))
                            pygame.display.update()
                            time.sleep(1)
                            pygame.quit()
                            return True

    intervalTime = 0
    while True:
        # 处理关闭游戏和调用加生命方法
        if handleEvent():
            break
        # 调用画图片方法
        drawAll()
        # 调用生成黑心的方法
        born()
        # 调用移动方法
        moveAll()
        # 调用outSide方法
        outSide()
        # 调用碰撞检测方法
        if collision():
            break
        # 结束
        if intervalTime >= 25:
            canvas.blit(bg3, (0, 0))
            pygame.display.update()
            end = time.time()
            while time.time() - end <= 1:
                pass
            pygame.quit()
            break
        # 填充文字
        end = time.time()
        intervalTime = int(end - start)
        fillText('你坚持了:' + str(intervalTime) + '年', (40, 20))
        fillText('机会:' + str(rlove.life), (400, 20))
        # 更新屏幕内容
        pygame.display.update()
