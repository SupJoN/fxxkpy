# coding:utf-8
# 动态壁纸
class Dynamic(object):
    '''
    Windows下的动态壁纸类

    只有x86架构的64位Windows可以运行，其他系统会报错
    self.start 方法开始显示壁纸
    self.stop 方法结束显示壁纸

    属性:
        video: 视频绝对路径
        player: ffplay 播放器的绝对路径，$default 为 \\wallpaper\\ffplay 下的 ffplay.exe
        command: 运行参数，$default 为默认参数，如果改变了参数，可以用 $video 代替视频绝对路径
        SetDpi: 改变缩放设置需要用的程序
        userdpi: self.__getdpi 函数获取到的 dpi
        stop_threads: 停止线程的参数
        display_thread: 显示线程
        back_thread: 还原缩放设置线程
        main_thread: 主线程
    '''

    def __init__(self, video: str, player: str = "$default", command: str = "$default"):
        # 导入库
        import os as __os
        import time as __time
        import platform as __platform
        import threading as __threading
        import win32api as __win32api
        import win32gui as __win32gui
        import win32con as __win32con
        import win32print as __win32print
        self.__os = __os
        self.__time = __time
        self.__platform = __platform
        self.__threading = __threading
        self.__win32api = __win32api
        self.__win32gui = __win32gui
        self.__win32con = __win32con
        self.__win32print = __win32print
        # 判断系统是否为x86架构的64位Windows
        if self.__platform.system() == "Windows" and self.__platform.machine() == "AMD64":
            self.video = video
            self.player = player if player != "$default" else f"{self.__os.path.split(self.__os.path.abspath(__file__))[0]}\\wallpaper\\ffplay\\ffplay.exe"
            self.command = command.replace(
                "$video", video, 1) if command != "$default" else f"{video} -noborder -fs -loop 0 -loglevel quiet"
            self.SetDpi = f"{self.__os.path.split(self.__os.path.abspath(__file__))[0]}\\wallpaper\\SetDpi.exe"
            self.userdpi = self.__getdpi()
            self.stop_threads = False
            self.display_thread = None
            self.back_thread = None
            self.main_thread = None
        else:
            raise Exception(
                f"CompatibilityError: {self.__platform.system} is not compatible with {self.__platform.machine()}")

    # 获取真实的分辨率
    def __get_real_resolution(self):
        hDC = self.__win32gui.GetDC(0)
        # 横向分辨率
        w = self.__win32print.GetDeviceCaps(
            hDC, self.__win32con.DESKTOPHORZRES)
        # 纵向分辨率
        h = self.__win32print.GetDeviceCaps(
            hDC, self.__win32con.DESKTOPVERTRES)
        return w, h

    # 获取缩放后的分辨率
    def __get_screen_size(self):
        w = self.__win32api.GetSystemMetrics(0)
        h = self.__win32api.GetSystemMetrics(1)
        return w, h

    # 获取DPI
    def __getdpi(self):
        real_resolution = self.__get_real_resolution()
        screen_size = self.__get_screen_size()
        screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
        screen_scale_rate = screen_scale_rate * 100
        return screen_scale_rate

    # 缩放设置为100%
    def __change(self):
        if self.userdpi == 100:
            return False
        else:
            self.__win32api.ShellExecute(0, 'open', self.SetDpi, ' 100', '', 1)
            return True

    # 缩放自动调回初始值
    def __back(self):
        self.__win32api.ShellExecute(
            0, 'open', self.SetDpi, str(self.userdpi), '', 1)

    # 播放视频
    def __play(self):
        self.__os.popen(f"{self.player} {self.command}")

    # 隐藏WorkerW
    def __hide(self, hwnd, hwnds):
        hdef = self.__win32gui.FindWindowEx(
            hwnd, 0, "SHELLDLL_DefView", None)  # 枚举窗口寻找特定类
        if hdef != 0:
            workerw = self.__win32gui.FindWindowEx(
                0, hwnd, "WorkerW", None)  # 找到hdef后寻找WorkerW
            self.__win32gui.ShowWindow(
                workerw, self.__win32con.SW_HIDE)  # 隐藏WorkerW
            while True:
                self.__time.sleep(100)  # 进入循环防止壁纸退出

    # 显示壁纸
    def __display(self):
        self.__play()
        self.__time.sleep(0.5)
        progman = self.__win32gui.FindWindow(
            "Progman", "Program Manager")  # 寻找Progman
        self.__win32gui.SendMessageTimeout(
            progman, 0x52C, 0, 0, 0, 0)  # 发送0x52C消息
        videowin = self.__win32gui.FindWindow("SDL_app", None)  # 寻找ffplay 播放窗口
        self.__win32gui.SetParent(videowin, progman)  # 设置子窗口
        self.__win32gui.EnumWindows(self.__hide, None)  # 枚举窗口，回调hide函数

    # 主函数
    def __main(self):
        self.__time.sleep(1)
        self.display_thread = self.__threading.Thread(
            target=self.__display, daemon=True)
        self.back_thread = self.__threading.Thread(
            target=self.__back, daemon=True)
        self.display_thread.start()
        self.__time.sleep(1)
        self.back_thread.start()
        while not self.stop_threads:
            pass
        return

    # 开始函数
    def start(self):
        self.main_thread = self.__threading.Thread(
            target=self.__main if self.__change() else self.__display)
        self.main_thread.start()

    # 停止函数
    def stop(self):
        self.stop_threads = True
        self.main_thread.join()
