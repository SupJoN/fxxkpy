# coding:utf-8
# 动态壁纸
class Dynamic(object):
    '''
    Windows 下的动态壁纸类

    只有 x86 架构的 64 位 Windows 可以运行, 其他系统会报错

    `self.start` 方法开始显示壁纸

    属性:
        `video`: 视频绝对路径
        `player`: `ffplay` 播放器的绝对路径, `$default` 为 `\\wallpaper\\ffplay` 下的 `ffplay.exe`
        `command`: 运行参数, `$default` 为默认参数, 如果改变了参数, 可以用 `$video` 代替视频绝对路径
        `daemon`: `display_thread` 的 `daemon` 属性
        `SetDpi`: 改变缩放设置需要用的程序
        `userdpi`: `self.__getdpi` 函数获取到的 dpi
        `display_thread`: 显示线程

    注意:
        程序运作是可能会改变缩放率, 忽略即可, 程序运行要十秒左右的时间, 最好啥都不干
    '''
    def __init__(self, video: str, player: str = "$default", command: str = "$default", daemon: bool = True) -> None:
        import os
        import platform
        import threading

        if isinstance(video, str) and isinstance(player, str) and isinstance(command, str):
            if platform.system() == "Windows" and platform.machine() == "AMD64":
                path: str = os.path.split(os.path.abspath(__file__))[0]
                self.video: str = video
                self.player: str = player if player != "$default" else f"{path}\\wallpaper\\ffplay\\ffplay.exe"
                self.command: str = command if command != "$default" else f"$video -noborder -fs -loop 0 -loglevel quiet"
                self.daemon: bool = daemon
                self.SetDpi: str = f"{path}\\wallpaper\\SetDpi.exe"
                self.userdpi: float = self.__getdpi()
                self.display_thread: threading.Thread | None = None
            else:
                raise Exception(f"CompatibilityError: {platform.system()} is not compatible with {platform.machine()}")
        else:
            raise TypeError("only str is supported")

    # 获取真实的分辨率
    def __get_real_resolution(self) -> tuple[int, int]:
        import win32con
        import win32gui
        import win32print
        hDC: int = win32gui.GetDC(0)
        w: int = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        h: int = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
        return w, h

    # 获取缩放后的分辨率
    def __get_screen_size(self) -> tuple[int, int]:
        import win32api
        w: int = win32api.GetSystemMetrics(0)
        h: int = win32api.GetSystemMetrics(1)
        return w, h

    # 获取DPI
    def __getdpi(self) -> float:
        real_resolution: tuple[int, int] = self.__get_real_resolution()
        screen_size: tuple[int, int] = self.__get_screen_size()
        screen_scale_rate: float = round(real_resolution[0] / screen_size[0], 2) * 100
        return screen_scale_rate

    # 缩放设置为100%
    def __change(self) -> bool:
        import win32api
        if self.userdpi == 100:
            return False
        else:
            win32api.ShellExecute(0, "open", self.SetDpi, " 100", "", 1)
            return True

    # 缩放自动调回初始值
    def __back(self) -> None:
        import win32api
        win32api.ShellExecute(0, "open", self.SetDpi, str(self.userdpi), "", 1)

    # 播放视频
    def __play(self) -> None:
        import os
        os.popen(f"{self.player} {self.command.replace('$video', self.video)}")

    # 隐藏WorkerW
    def __hide(self, hwnd: int, hwnds: None) -> None:
        import time

        import win32con
        import win32gui

        hdef: int = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)  # 枚举窗口寻找特定类
        if hdef != 0:
            workerw: int = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)  # 找到hdef后寻找WorkerW
            win32gui.ShowWindow(workerw, win32con.SW_HIDE)  # 隐藏WorkerW
            while True:
                time.sleep(100)  # 进入循环防止壁纸退出

    # 显示壁纸
    def __display(self) -> None:
        import time

        import win32gui

        self.__play()
        time.sleep(0.5)
        progman: int = win32gui.FindWindow("Progman", "Program Manager")  # 寻找Progman
        win32gui.SendMessageTimeout(progman, 0x52C, 0, 0, 0, 0)  # 发送0x52C消息
        videowin: int = win32gui.FindWindow("SDL_app", None)  # 寻找ffplay 播放窗口
        win32gui.SetParent(videowin, progman)  # 设置子窗口
        win32gui.EnumWindows(self.__hide, None)  # 枚举窗口, 回调hide函数

    # 开始函数
    def start(self) -> None:
        from threading import Thread
        from time import sleep
        self.display_thread: Thread = Thread(target=self.__display, daemon=self.daemon)
        if self.__change():
            sleep(0.5)
            self.display_thread.start()
            sleep(0.5)
            self.__back()
        else:
            self.display_thread.start()

    # 存在
    def alive(self) -> bool:
        return self.display_thread.is_alive()

    # __call__ 函数
    def __call__(self) -> None:
        self.start()
