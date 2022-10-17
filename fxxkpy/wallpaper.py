# coding:utf-8
# 动态壁纸
class Dynamic(object):
    '''
    Windows下的动态壁纸类

    只有x86架构的64位Windows可以运行, 其他系统会报错

    self.start 方法开始显示壁纸

    self.stop 方法结束显示壁纸

    属性:
        video: 视频绝对路径
        player: ffplay 播放器的绝对路径, $default 为 \\wallpaper\\ffplay 下的 ffplay.exe
        command: 运行参数, $default 为默认参数, 如果改变了参数, 可以用 $video 代替视频绝对路径
        SetDpi: 改变缩放设置需要用的程序
        userdpi: self.__getdpi 函数获取到的 dpi
        stop_threads: 停止线程的参数
        display_thread: 显示线程
        back_thread: 还原缩放设置线程
        main_thread: 主线程

    注意:
        程序运作是可能会改变缩放率, 忽略即可, 程序运行要十秒左右的时间, 最好啥都不干
    '''
    def __init__(self, video: str, player: str = "$default", command: str = "$default") -> None:
        import os
        import platform
        import threading

        if platform.system() == "Windows" and platform.machine() == "AMD64":
            self.video: str = video
            self.player: str = player if player != "$default" else os.path.join(os.path.split(os.path.abspath(__file__))[0], "\\wallpaper\\ffplay\\ffplay.exe")
            self.command: str = command.replace("$video", video, 1) if command != "$default" else f"{video} -noborder -fs -loop 0 -loglevel quiet"
            self.SetDpi: str = os.path.join(os.path.split(os.path.abspath(__file__))[0], "\\wallpaper\\SetDpi.exe")
            self.userdpi: float = self.__getdpi()
            self.stop_threads: bool = False
            self.display_thread: None | threading.Thread = None
            self.back_thread: None | threading.Thread = None
            self.main_thread: None | threading.Thread = None
        else:
            raise Exception(f"CompatibilityError: {platform.system} is not compatible with {platform.machine()}")

    # 获取真实的分辨率
    def __get_real_resolution(self) -> tuple:
        import win32con
        import win32gui
        import win32print

        hDC = win32gui.GetDC(0)
        print(type(hDC))
        # 横向分辨率
        w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        # 纵向分辨率
        h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)

        return w, h

    # 获取缩放后的分辨率
    def __get_screen_size(self) -> tuple:
        import win32api

        w = win32api.GetSystemMetrics(0)
        h = win32api.GetSystemMetrics(1)

        return w, h

    # 获取DPI
    def __getdpi(self) -> float:
        real_resolution = self.__get_real_resolution()
        screen_size = self.__get_screen_size()
        screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
        screen_scale_rate = screen_scale_rate * 100
        return screen_scale_rate

    # 缩放设置为100%
    def __change(self) -> bool:
        import win32api

        if self.userdpi == 100:
            return False
        else:
            win32api.ShellExecute(0, 'open', self.SetDpi, ' 100', '', 1)
            return True

    # 缩放自动调回初始值
    def __back(self) -> None:
        import win32api

        win32api.ShellExecute(0, 'open', self.SetDpi, str(self.userdpi), '', 1)

    # 播放视频
    def __play(self) -> None:
        import os

        os.popen(f"{self.player} {self.command}")

    # 隐藏WorkerW
    def __hide(self, hwnd: int, hwnds: None) -> None:
        import time

        import win32con
        import win32gui

        hdef = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)  # 枚举窗口寻找特定类
        if hdef != 0:
            workerw = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)  # 找到hdef后寻找WorkerW
            win32gui.ShowWindow(workerw, win32con.SW_HIDE)  # 隐藏WorkerW
            while True:
                time.sleep(100)  # 进入循环防止壁纸退出

    # 显示壁纸
    def __display(self) -> None:
        import time

        import win32gui

        self.__play()
        time.sleep(0.5)
        progman = win32gui.FindWindow("Progman", "Program Manager")  # 寻找Progman
        win32gui.SendMessageTimeout(progman, 0x52C, 0, 0, 0, 0)  # 发送0x52C消息
        videowin = win32gui.FindWindow("SDL_app", None)  # 寻找ffplay 播放窗口
        win32gui.SetParent(videowin, progman)  # 设置子窗口
        win32gui.EnumWindows(self.__hide, None)  # 枚举窗口, 回调hide函数

    # 主函数
    def __main(self) -> None:
        import threading
        import time

        time.sleep(0.5)
        self.display_thread: threading.Thread = threading.Thread(target=self.__display, daemon=True)
        self.back_thread: threading.Thread = threading.Thread(target=self.__back, daemon=True)
        self.display_thread.start()
        time.sleep(0.5)
        self.back_thread.start()
        while not self.stop_threads:
            pass
        return

    # 开始函数
    def start(self) -> None:
        import threading

        self.main_thread: threading.Thread = threading.Thread(target=self.__main if self.__change() else self.__display)
        self.main_thread.start()

    # 停止函数
    def stop(self) -> None:
        self.stop_threads: bool = True
        self.main_thread.join()
