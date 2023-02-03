# coding:utf-8
from tempfile import gettempdir as _gettempdir

__all__: tuple[str, ...] = ("record", )


# 记录数据
def record(data_path: str = f"{_gettempdir()}/fxxkpy_enigma_data.txt") -> None:
    '''
    通过网页编辑恩格玛机

    在 `HTTPServer` 开启后, `KeyboardInterrupt` 错误可以打断编辑

    参数:
        `data_path` 为结果文件的保存路径, 默认为 TEMP 文件夹下的 fxxkpy_enigma_data.txt

    Bug:
        处理请求是可能有 `ConnectionAbortedError` , 已用 `try` 解决
        `httpd` 变量创建时
    '''
    import os
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from threading import Thread
    from time import time
    from typing import Callable
    from urllib.parse import parse_qs, urlparse

    # host 配置
    hosts: list[str, int] = ["", 8098]

    # 0: 服务未开始
    # 1: 服务已开始
    # 2: 服务已结束
    status: list[int] = [0]

    # 提示语
    def prompt() -> None:
        data: tuple[tuple[tuple[Callable[[], str], ...], ...]] = ((
            (
                lambda: ".  \b\b\b",
                lambda: ".. \b\b\b",
                lambda: "...\b\b\b",
            ),
            (
                lambda: "\b|",
                lambda: "\b/",
                lambda: "\b—",
                lambda: "\b\\",
            ),
        ), (
            (lambda: "等待服务开启中 ", ),
            (lambda: f"\r请访问 http://localhost:{hosts[1]} 以编辑恩格玛机\n正在等待编辑完成  ", ),
        ))
        last: int = -1
        now: int = status[0]
        end_time: tuple[float, bool] = (float("INF"), False)
        while time() - end_time[0] < 0.5:
            if last != (now - 2 or -1) + 2:
                first: bool = True
                last: int = now
            else:
                first: bool = False

            for item in data[first][(now - 2 or -1) + 2]:
                print(item(), end="", flush=True)
                if not first:
                    start: float = time()
                    while time() - start < 0.2:
                        if not end_time[1] and status[0] == 2:
                            end_time: tuple[float, bool] = (time(), True)
                        if time() - end_time[0] >= 0.5:
                            return

            if end_time[1] and status[0] == 2:
                end_time: tuple[float, bool] = (time(), True)

            now: int = status[0]

    # 结束时间
    end_time: float = float("INF")

    # 提示语线程
    prompt_thread: Thread = Thread(target=prompt, daemon=True)
    prompt_thread.start()

    # 文件夹路径
    path: str = os.path.split(os.path.abspath(__file__))[0]

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            request: dict[str, str | dict[str, list[str]]] = {
                "path": (url := urlparse(self.path)).path,
                "query": parse_qs(url.query),
            }

            try:
                # 处理 GET 请求
                if request["path"] == "/":
                    # 跳转到 /index
                    self.send_response(301)
                    self.send_header("Location", "/index")
                    self.end_headers()

                elif request["path"] == "/index":
                    # 返回 index.html 文件
                    with open(os.path.join(path, "static", "index.html"), "rb") as f:
                        content: bytes = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Content-Length", len(content))
                    self.end_headers()
                    self.wfile.write(content)

                elif request["path"] == "/apply":
                    # 记录结果
                    with open(data_path, "w") as file:
                        file.write(request["query"]["data"][0] if "data" in request["query"] else "None")
                    # 记录状态
                    status[0]: int = 2
                    # 记录结束时间
                    nonlocal end_time
                    end_time = time()

                    # 返回 apply.html 文件
                    with open(os.path.join(path, "static", "apply.html"), "rb") as f:
                        content: bytes = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Content-Length", len(content))
                    self.end_headers()
                    self.wfile.write(content)

                elif request["path"] == "/vue.js":
                    # 返回 vue.js 文件
                    with open(os.path.join(path, "static", "vue.js"), "rb") as f:
                        content: bytes = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/javascript")
                    self.send_header("Content-Length", len(content))
                    self.end_headers()
                    self.wfile.write(content)

                elif request["path"] == "/favicon.ico":
                    # 返回 favicon.ico 文件
                    with open(os.path.join(path, "static", "favicon.ico"), "rb") as f:
                        content: bytes = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "image/x-icon")
                    self.send_header("Content-Length", len(content))
                    self.end_headers()
                    self.wfile.write(content)

                elif request["path"] == "/game":
                    # 返回 game.html 文件
                    with open(os.path.join(path, "static", "game.html"), "rb") as f:
                        content: bytes = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Content-Length", len(content))
                    self.end_headers()
                    self.wfile.write(content)

                else:
                    # 返回 404.html 文件
                    with open(os.path.join(path, "static", "404.html"), "rb") as f:
                        content: bytes = f.read()
                    self.send_response(404)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Content-Length", len(content))
                    self.end_headers()
                    self.wfile.write(content)
            except ConnectionAbortedError:
                pass

        # 不显示输出
        def log_message(self, format: str, *args: str) -> None:
            pass

    httpd: ThreadingHTTPServer = ThreadingHTTPServer(tuple(hosts), RequestHandler)
    httpd.timeout = 0.005

    try:
        status[0]: int = 1
        while status[0] != 2 or time() - end_time <= 0.5:
            httpd.handle_request()
        prompt_thread.join()
        print("\r恩格玛机已编辑完毕")
    except KeyboardInterrupt:
        status[0]: int = 2
        prompt_thread.join()
        print("\r恩格玛机的编辑以被人为结束")


del _gettempdir
