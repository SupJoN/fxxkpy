# coding:utf-8
import tempfile

tempdir = tempfile.gettempdir()

del tempfile


# 记录数据
def record(DataPath: str = f"{tempdir}/fxxkpy_enigma_data.txt", confirm: bool = False) -> None:
    from threading import Thread
    from threading import enumerate as thread_enumerate
    from time import sleep, time
    from typing import Callable

    # 网页
    def bottle_run(stop_thread: Callable[[Thread], None], apply_thread: Thread) -> None:
        import os

        import bottle

        path: str = os.path.split(os.path.abspath(__file__))[0]

        @bottle.route("/")
        def index_redirect() -> bottle.HTTPResponse:
            bottle.redirect("/index", code=301)

        @bottle.route("/index")
        def index() -> bottle.HTTPResponse:
            return bottle.static_file("index.html", root=os.path.join(path, "static"))

        @bottle.route("/favicon.ico")
        def ico() -> bottle.HTTPResponse:
            return bottle.static_file("favicon.ico", root=os.path.join(path, "static"))

        @bottle.route("/vue.js")
        def vue() -> bottle.HTTPResponse:
            return bottle.static_file("vue.js", root=os.path.join(path, "static"))

        @bottle.get("/apply")
        def apply() -> bottle.HTTPResponse:
            try:
                data = bottle.request.query["data"]
            except:
                data = "None"
            with open(DataPath, "w") as file:
                file.write(data)

            stop_thread(apply_thread)

            return bottle.static_file("apply.html", root=os.path.join(path, "static")),

        @bottle.route("/game")
        def game404() -> bottle.HTTPResponse:
            return bottle.static_file("game.html", root=os.path.join(path, "static"))

        @bottle.error(404)
        def error404(error: bottle.HTTPError) -> bottle.HTTPResponse:
            response: bottle.HTTPResponse = bottle.static_file("404.html", root=os.path.join(path, "static"))
            response.status: int = 404
            return response

        bottle.run(host="0.0.0.0", port=8098, quiet=True)

    # 被检测线程
    def apply() -> None:
        while True:
            pass

    # 停止线程
    def stop_thread(thread: Thread) -> None:
        from ctypes import c_long, py_object, pythonapi

        pythonapi.PyThreadState_SetAsyncExc(c_long(thread.ident), py_object(SystemExit))

    apply_thread: Thread = Thread(target=apply)
    bottle_run_thread: Thread = Thread(target=bottle_run, args=(stop_thread, apply_thread))
    apply_thread.start()
    bottle_run_thread.start()

    try:
        print("等待服务开启中 ", end="")
        start = time()
        while time() - start <= 7.5:
            for item in (".  \b\b\b", ".. \b\b\b", "...\b\b\b"):
                print(item, end="")
                sleep(0.2)

        print("\r请访问 http://localhost:8098 以编辑恩格玛机")

        while apply_thread.is_alive():
            for item in ("|", "/", "—", "\\"):
                print(f"\r正在等待编辑完成 {item}", end="")
                sleep(0.2)

    except KeyboardInterrupt:
        stop_thread(apply_thread)
        stop_thread(bottle_run_thread)
        print("\r恩格玛机的编辑以被人为结束")
        return

    stop_thread(bottle_run_thread)
    print("\r恩格玛机已编辑完毕")
    return
