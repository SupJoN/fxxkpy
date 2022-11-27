# coding:utf-8
# 飞机大战
def AircraftWar(life: int = 5) -> None:
    # 导入模块
    import os
    import random
    import time
    import typing
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""  # 隐藏pygame的import欢迎显示
    import pygame

    # 初始化pygame环境
    pygame.init()

    # 创建一个长宽分别为1200/715的白色窗口
    x = 80
    y = 27
    os.environ["SDL_VIDEO_WINDOW_POS"]: str = f"{x},{y}"
    canvas: pygame.Surface = pygame.display.set_mode((1200, 715))
    canvas.fill((255, 255, 255))

    # 设置窗口标题
    pygame.display.set_caption("飞机大战")

    # 敌飞机图片数组
    file: str = os.path.split(os.path.abspath(__file__))[0]
    e1: typing.List[pygame.Surface] = []
    e1.append(pygame.image.load(f"{file}/game/AircraftWar/enemy1.png"))
    e1.append(pygame.image.load(f"{file}/game/AircraftWar/enemy1_down1.png"))
    e1.append(pygame.image.load(f"{file}/game/AircraftWar/enemy1_down2.png"))
    e1.append(pygame.image.load(f"{file}/game/AircraftWar/enemy1_down3.png"))
    e1.append(pygame.image.load(f"{file}/game/AircraftWar/enemy1_down4.png"))
    e1.append(pygame.image.load(f"{file}/game/AircraftWar/enemy1_down5.png"))
    e2: typing.List[pygame.Surface] = []
    e2.append(pygame.image.load(f"{file}/game/AircraftWar/enemy2.png"))
    e2.append(pygame.image.load(f"{file}/game/AircraftWar/enemy2_down1.png"))
    e2.append(pygame.image.load(f"{file}/game/AircraftWar/enemy2_down2.png"))
    e2.append(pygame.image.load(f"{file}/game/AircraftWar/enemy2_down3.png"))
    e2.append(pygame.image.load(f"{file}/game/AircraftWar/enemy2_down4.png"))
    e2.append(pygame.image.load(f"{file}/game/AircraftWar/enemy2_down5.png"))
    e3: typing.List[pygame.Surface] = []
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_1.png"))
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_2.png"))
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_down1.png"))
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_down2.png"))
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_down3.png"))
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_down4.png"))
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_down5.png"))
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_down6.png"))
    e3.append(pygame.image.load(f"{file}/game/AircraftWar/enemy3_down7.png"))
    # 英雄机图片数组
    h: typing.List[pygame.Surface] = []
    h.append(pygame.image.load(f"{file}/game/AircraftWar/hero.png"))
    h.append(pygame.image.load(f"{file}/game/AircraftWar/hero_down1.png"))
    h.append(pygame.image.load(f"{file}/game/AircraftWar/hero_down2.png"))
    h.append(pygame.image.load(f"{file}/game/AircraftWar/hero_down3.png"))
    h.append(pygame.image.load(f"{file}/game/AircraftWar/hero_down4.png"))
    # 背景图片
    bg: pygame.Surface = pygame.image.load(f"{file}/game/AircraftWar/bg.jpg")
    # 子弹图片
    b: typing.List[pygame.Surface] = []
    b.append(pygame.image.load(f"{file}/game/AircraftWar/bullet.png"))
    # 开始游戏图片
    startgame: pygame.Surface = pygame.image.load(f"{file}/game/AircraftWar/startGame.png")
    # logo图片
    logo: pygame.Surface = pygame.image.load(f"{file}/game/AircraftWar/LOGO.png")
    # 暂停图片
    pause: pygame.Surface = pygame.image.load(f"{file}/game/AircraftWar/game_pause_nor.png")
    score: pygame.Surface = pygame.image.load(f"{file}/game/AircraftWar/score.png")
    over: pygame.Surface = pygame.image.load(f"{file}/game/AircraftWar/over.png")

    # 键盘事件检测
    def handleEvent() -> typing.Optional[bool]:
        for event in pygame.event.get():
            event: pygame.event.Event
            if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return True
            # 监听鼠标移动事件
            if event.type == pygame.MOUSEMOTION:
                # 根据鼠标的坐标修改英雄机的坐标
                # 使用get_width函数可以获取图片的宽度
                if GameVar.state == GameVar.STATES["RUNNING"]:
                    GameVar.hero.x: int = event.pos[0] - GameVar.hero.width / 2
                    GameVar.hero.y: int = event.pos[1] - GameVar.hero.height / 2
                # 鼠标移入移出事件切换状态
                if isMouseOut(event.pos[0], event.pos[1]):
                    if GameVar.state == GameVar.STATES["RUNNING"]:
                        GameVar.state: int = GameVar.STATES["PAUSE"]
                if isMouseOver(event.pos[0], event.pos[1]):
                    if GameVar.state == GameVar.STATES["PAUSE"]:
                        GameVar.state: int = GameVar.STATES["RUNNING"]

            # 点击左键切换为运行状态
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if GameVar.state == GameVar.STATES["START"]:
                    GameVar.state: int = GameVar.STATES["RUNNING"]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if GameVar.state == GameVar.STATES["GAME_OVER"]:
                    GameVar.score: int = 0
                    GameVar.heroes: int = 4
                    GameVar.state: int = GameVar.STATES["START"]

    # 画图
    def draw(img: pygame.Surface, x: int, y: int) -> None:
        canvas.blit(img, (x, y))

    # 工具方法-判断时间间隔是否到了
    def isActionTime(lastTime: float, interval: float) -> bool:
        return True if lastTime == 0 else time.time() - lastTime >= interval

    # 工具方法-写文字方法
    def renderText(text: str, position: tuple[int, int], view: pygame.Surface = canvas) -> None:
        view.blit(pygame.font.Font(f"{file}/game/AircraftWar/font.ttf", 30).render(text, True, (255, 255, 255)), position)

    # 工具方法-判断鼠标是否移出了游戏区域
    def isMouseOut(x: int, y: int) -> bool:
        return x >= 1190 or x <= 0 or y > 700 or y <= 0

    # 工具方法-判断鼠标是否移入了游戏区域
    def isMouseOver(x: int, y: int) -> bool:
        return x > 0 and x < 1150 and y > 1 and y < 648

    # 定义Sky类
    class Sky(object):
        def __init__(self):
            self.width: int = 480
            self.height: int = 680
            self.img: pygame.Surface = bg
            self.x1: int = 0
            self.y1: int = 0
            self.x2: int = 0
            self.y2: int = -self.height

        def paint(self) -> None:
            draw(self.img, self.x1, self.y1)
            draw(self.img, self.x2, self.y2)

        def step(self) -> None:
            self.y1: int = self.y1 + 1
            self.y2: int = self.y2 + 1
            if self.y1 > self.height:
                self.y1: int = -self.height
            if self.y2 > self.height:
                self.y2: int = -self.height

    # 定义父类FlyingObject
    class FlyingObject(object):
        def __init__(self, x: int, y: int, width: int, height: int, life: int, frames: list[pygame.Surface], baseFrameCount: int) -> None:
            self.x: int = x
            self.y: int = y
            self.score: int = 0
            self.width: int = width
            self.height: int = height
            self.life: int = life
            # 敌飞机移动的时间间隔
            self.lastTime: float = 0
            self.interval: float = 0.
            # 添加掉落属性和删除属性
            self.down: bool = False
            self.canDelete: bool = False
            # 实现动画所需属性
            self.frames: list[pygame.Surface] = frames
            self.frameIndex: int = 0
            self.img: pygame.Surface = self.frames[self.frameIndex]
            self.frameCount: int = baseFrameCount

        # 画图方法
        def paint(self) -> None:
            draw(self.img, self.x, self.y)

        # 移动方法
        def step(self) -> None:
            # 判断是否到了移动的时间间隔
            if isActionTime(self.lastTime, self.interval):
                self.lastTime = time.time()
                # 控制移动速度
                self.y = self.y + 5

        # 碰撞检测方法
        def hit(self, component: "FlyingObject") -> bool:
            return component.x > self.x - component.width and component.x < self.x + self.width and component.y > self.y - component.height and component.y < self.y + self.height

        # 处理碰撞发生后要做的事
        def bang(self) -> None:
            self.life -= 1
            if self.life == 0:
                # 生命值为0时将down置为True
                self.down: bool = True
                # 将frameIndex切换为销毁动画的第一张
                self.frameIndex: int = self.frameCount

                if hasattr(self, "score"):
                    GameVar.score += self.score

        # 越界处理
        def outOfBounds(self) -> bool:
            return self.y > 650

        # 实现动画
        def animation(self) -> None:
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
        def __init__(self, x: int, y: int, width: int, height: int, type: int, life: int, score: int, frames: list[pygame.Surface], baseFrameCount: int) -> None:
            super().__init__(x, y, width, height, life, frames, baseFrameCount)
            self.x: int = random.randint(0, 1300 - self.width)
            self.y: int = -self.height
            self.type: int = type
            self.score: int = score

    # 定义Hero类
    class Hero(FlyingObject):
        def __init__(self, x: int, y: int, width: int, height: int, life: int, frames: list[pygame.Surface], baseFrameCount: int) -> None:
            super().__init__(x, y, width, height, life, frames, baseFrameCount)
            self.width: int = 60
            self.height: int = 75
            self.x: int = 450 + 480 / 2 - self.width / 2
            self.y: int = 650 - self.height - 30

        def paint(self) -> None:
            draw(self.img, self.x, self.y)

        def shoot(self) -> None:
            GameVar.bullets.append(Bullet(self.x + self.width / 2 - 20, self.y, 9, 21, 1, b, 1))
            GameVar.bullets.append(Bullet(self.x + self.width / 2 + 10, self.y, 9, 21, 1, b, 1))

    # 定义Bullet类
    class Bullet(FlyingObject):
        def __init__(self, x: int, y: int, width: int, height: int, life: int, frames: list[pygame.Surface], baseFrameCount: int) -> None:
            super().__init__(x, y, width, height, life, frames, baseFrameCount)

        # 重写step方法
        def step(self) -> None:
            self.y -= 10

        # 重写判断是否越界的方法
        def outOfBounds(self) -> bool:
            return self.y < -self.height

    # 生成组件
    def componentEnter() -> None:
        # 判断是否到了产生敌飞机的时间
        if isActionTime(GameVar.lastTime, GameVar.interval):
            GameVar.lastTime: float = time.time()

            # 根据随机整数的值生成不同的敌飞机
            n: int = random.randint(0, 9)
            if n <= 7:
                # 因为列表初始值为空，所以这里可以使用append或insert进行添加元素，append会将新增的追加到末尾，但insert会将新增的插入到指定位置
                GameVar.enemies.append(Enemy(random.randint(0, 1200 - 57), -45, 57, 45, 1, 1, 1, e1, 1))
            elif n == 8:
                GameVar.enemies.append(Enemy(random.randint(0, 1200 - 50), -68, 50, 68, 2, 3, 5, e2, 1))
            elif n == 9 and len(GameVar.enemies) == 0 or GameVar.enemies[0].type != 3:
                # 将打飞机放在列表中索引为0的位置
                GameVar.enemies.insert(0, Enemy(random.randint(0, 1200 - 169), -258, 169, 258, 3, 10, 20, e3, 2))

    # 画组件方法
    def paintComponent() -> None:
        # 判断是否到了飞行物重绘的时间
        if isActionTime(GameVar.paintLastTime, GameVar.paintInterval):
            GameVar.paintLastTime: float = time.time()

            # 调用sky对象的paint方法
            GameVar.sky.paint()
            # 画敌飞机并实现敌飞机移动
            for enemy in GameVar.enemies:
                enemy.paint()
            # 画英雄机
            GameVar.hero.paint()
            # 画子弹
            for bullet in GameVar.bullets:
                bullet.paint()
            # 写分数和生命值
            draw(score, 720 + 210, 10)
            renderText(str(GameVar.score), (780 + 305, 25))
            renderText(str(GameVar.heroes), (780 + 305, 58))

    # 组件移动方法
    def componentStep() -> None:
        # 调用sky对象的step方法
        GameVar.sky.step()
        # 调用enemy对象的step方法
        for enemy in GameVar.enemies:
            enemy.step()
        # 调用bullet对象的step方法
        for bullet in GameVar.bullets:
            bullet.step()

    # 检测组件碰撞
    def checkHit() -> None:
        # 判断敌飞机是否和英雄机相撞
        for enemy in GameVar.enemies:
            if enemy.down != True:
                if GameVar.hero.hit(enemy):
                    enemy.bang()
                    GameVar.hero.bang()
                for bullet in GameVar.bullets:
                    # 如果当前子弹是有效的子弹切碰撞则爆炸
                    if bullet.down != True and enemy.hit(bullet):
                        enemy.bang()
                        bullet.bang()

    # 删除无效组件
    def deleteComponent() -> None:
        # 删除无效的敌飞机
        for enemy in GameVar.enemies:
            if enemy.canDelete or enemy.outOfBounds():
                GameVar.enemies.remove(enemy)
        # 删除无效子弹
        for bullet in GameVar.bullets:
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
    def componentAnimation() -> None:
        # 敌飞机播放动画
        for enemy in GameVar.enemies:
            enemy.animation()
        # 子弹播放动画
        for bullet in GameVar.bullets:
            bullet.animation()
        # 英雄机播放动画
        GameVar.hero.animation()

    # 使用类属性存储游戏中的变量，以减少全局变量的数量
    class GameVar(object):
        # 英雄机对象
        hero: Hero = Hero(0, 0, 60, 75, 1, h, 1)
        # 敌机对象列表
        enemies: list[Enemy] = []
        # 天空背景对象
        sky: Sky = Sky()
        # 子弹列表
        bullets: list[Bullet] = []

        # 产生敌飞机的时间间隔
        lastTime: float = 0
        interval: float = 0.35  # 单位为秒
        # 重绘飞行物的时间间隔
        paintLastTime: float = 0
        paintInterval: float = 0.03
        # 分数和生命值
        score: int = 0
        heroes: int = life if isinstance(life, int) and life > 0 else 5
        # 控制游戏状态
        STATES: dict[str, int] = {"START": 1, "RUNNING": 2, "PAUSE": 3, "GAME_OVER": 4}
        state: int = STATES["START"]

    # 游戏状态控制
    def contralState():
        if GameVar.state == GameVar.STATES["START"]:
            GameVar.sky.paint()
            GameVar.sky.step()
            draw(logo, 200, 200)
            draw(startgame, 460, 450)
        elif GameVar.state == GameVar.STATES["RUNNING"]:
            componentEnter()
            # 画组件
            paintComponent()
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
            paintComponent()
            GameVar.sky.step()
            draw(pause, 500, 250)
        elif GameVar.state == GameVar.STATES["GAME_OVER"]:
            paintComponent()
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
def HeartWar(life: int = 5, year: int = 25) -> None:
    import os
    import random
    import time
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""  # 隐藏pygame的import欢迎显示
    import pygame

    # 初始化pygame环境
    pygame.init()

    # 创建一个长宽分别为480/650的窗口
    os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (300, 50)
    canvas: pygame.Surface = pygame.display.set_mode((480, 650))

    # 设置窗口标题
    pygame.display.set_caption("红心大战")

    # 加载图片
    file: str = os.path.split(os.path.abspath(__file__))[0]
    bg1: pygame.Surface = pygame.image.load(f"{file}/game/HeartWar/bg1.png")
    bg2: pygame.Surface = pygame.image.load(f"{file}/game/HeartWar/bg2.png")
    bg3: pygame.Surface = pygame.image.load(f"{file}/game/HeartWar/bg3.png")
    loveR: pygame.Surface = pygame.image.load(f"{file}/game/HeartWar/loveRed.png")
    loveB: pygame.Surface = pygame.image.load(f"{file}/game/HeartWar/loveBlack.png")

    # 退出和加生命方法
    def handleEvent() -> bool:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    rlove.life: int = rlove.life + 1
        return False

    # 写文字方法
    def fillText(text: str, position: tuple[int, int]):
        TextFont: pygame.font.Font = pygame.font.Font(f"{file}/game/HeartWar/font.ttf", 25)
        newText: pygame.Surface = TextFont.render(text, True, (255, 0, 0))
        canvas.blit(newText, position)

    # 保存黑心变量
    mouseX: int = 200
    mouseY: int = 200
    bWidth: int = 18
    bHeight: int = 18
    bSpeed: int = 210

    # 创建黑心方法
    arrBlove: list["Blove"] = []

    def createBlove(bloveNum: int) -> None:
        for i in range(bloveNum):
            randPos: int = random.randint(0, 3)
            randX: float = random.random() * (480 - bWidth)
            randY: float = random.random() * (480 - bHeight)
            speed: float = random.random() * 200 + bSpeed
            if randPos == 0:
                arrBlove.append(Blove(randX, 0, loveB, bWidth, bHeight, mouseX, mouseY, speed))
            elif randPos == 1:
                arrBlove.append(Blove(462, randY, loveB, bWidth, bHeight, mouseX, mouseY, speed))
            elif randPos == 2:
                arrBlove.append(Blove(randX, 632, loveB, bWidth, bHeight, mouseX, mouseY, speed))
            elif randPos == 3:
                arrBlove.append(Blove(0, randY, loveB, bWidth, bHeight, mouseX, mouseY, speed))

    # 创建黑心类
    class Blove:
        def __init__(self, x: float, y: float, img: pygame.Surface, width: int, height: int, mouseX: int, mouseY: int, speed: float) -> None:
            self.x: float = x
            self.y: float = y
            self.img: pygame.Surface = img
            self.width: int = width
            self.height: int = height
            self.mouseX: int = mouseX
            self.mouseY: int = mouseY
            self.speed: float = speed
            self.xs: float = (self.mouseX - self.x) / speed
            self.ys: float = (self.mouseY - self.y) / speed

    # 创建红心类
    class Rlove(Blove):
        def __init__(self, x: int, y: int, img: pygame.Surface, width: int, height: int, mouseX: int, mouseY: int, speed: int, life: int, year: int, invincible_time: float) -> None:
            Blove.__init__(self, x, y, img, width, height, mouseX, mouseY, speed)
            self.__life: int = max(min(life, 13), 1)
            self.year: int = max(year, 1)
            self.invincible_time: float = invincible_time

        @property
        def life(self) -> int:
            return self.__life

        @life.setter
        def life(self, value: int) -> None:
            self.__life: int = max(min(value, 13), 1)

    # 创建红心对象
    start: float = time.time()
    rlove: Rlove = Rlove(mouseX, mouseY, loveR, 45, 25, 0, 0, 1, life if isinstance(life, int) else 5, year if isinstance(year, int) else 25, start)

    # 创建生成黑心对象方法
    bloveNum: int = 0

    def born() -> None:
        nonlocal bloveNum
        if len(arrBlove) <= 0:
            bloveNum += 1
            createBlove(bloveNum)

    # 创建画图片方法
    def drawAll() -> None:
        canvas.blit(bg2, (0, 0))
        # 绘制黑心
        for arrB in arrBlove:
            canvas.blit(arrB.img, (arrB.x, arrB.y))
        # 绘制红心图片
        canvas.blit(rlove.img, (rlove.x, rlove.y))

    # 创建移动方法
    def moveAll() -> None:
        nonlocal mouseX, mouseY
        for arrB in arrBlove:
            arrB.x: float = arrB.xs + arrB.x
            arrB.y: float = arrB.ys + arrB.y
        # 设置红心跟随鼠标移动
        mouseX, mouseY = pygame.mouse.get_pos()
        rlove.x: float = mouseX - rlove.width / 2
        rlove.y: float = mouseY - rlove.height / 2

    # 创建越界检测方法
    def outSide() -> None:
        for arrB in arrBlove:
            if (arrB.x + arrB.width < 0 or arrB.x > 480 or arrB.y + arrB.height < 0 or arrB.y > 650):
                arrBlove.remove(arrB)
            break

    # 创建碰撞检测方法
    def collision() -> bool:
        for arrB in arrBlove:
            if arrB.x + arrB.width > rlove.x and arrB.x < rlove.x + rlove.width and arrB.y + arrB.height > rlove.y and arrB.y < rlove.y + rlove.height and arrB.y + arrB.height > rlove.y and arrB.y < rlove.y + rlove.height and time.time() - rlove.invincible_time > 1:
                rlove.life: int = rlove.life - 1
                rlove.invincible_time = time.time()
                if rlove.life == 0:
                    canvas.blit(bg1, (0, 0))
                    pygame.display.update()
                    time.sleep(1)
                    pygame.quit()
                    return True
        return False

    intervalTime: int = 0
    # 处理关闭游戏和调用加生命方法
    while not handleEvent():
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
        if intervalTime >= rlove.year:
            canvas.blit(bg3, (0, 0))
            pygame.display.update()
            end: float = time.time()
            while time.time() - end <= 1:
                pass
            pygame.quit()
            break
        # 填充文字
        end: float = time.time()
        intervalTime: int = int(end - start)
        fillText(f"你坚持了:{intervalTime}年", (40, 20))
        fillText(f"机会:{rlove.life}", (390 if rlove.life // 10 else 400, 20))
        # 更新屏幕内容
        pygame.display.update()
