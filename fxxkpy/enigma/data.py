# coding:utf-8
import tempfile

tempdir = tempfile.gettempdir()

del tempfile


def record(DataPath: str = f"{tempdir}/fxxkpy_enigma_data.txt") -> None:
    import threading

    stop = False

    def run() -> None:
        import os

        import bottle

        path = os.path.split(os.path.abspath(__file__))[0]

        @bottle.route("/")
        def index() -> bottle.HTTPError | bottle.HTTPResponse:
            return bottle.static_file("index.html", root=os.path.join(path, "static"))

        @bottle.route("/favicon.ico")
        def ico() -> bottle.HTTPError | bottle.HTTPResponse:
            return bottle.static_file("favicon.ico", root=os.path.join(path, "static"))

        @bottle.get("/apply")
        def apply() -> bottle.HTTPError | bottle.HTTPResponse:
            try:
                data = bottle.request.query["data"]
            except:
                data = "None"
            with open(DataPath, "w") as file:
                file.write(data)

            nonlocal stop
            stop = True

            return bottle.static_file("apply.html", root=os.path.join(path, "static")),

        @bottle.route("/game")
        def game404() -> bottle.HTTPError | bottle.HTTPResponse:
            return bottle.static_file("game.html", root=os.path.join(path, "static"))

        @bottle.error(404)
        def error404(error) -> bottle.HTTPError | bottle.HTTPResponse:
            return bottle.static_file("404.html", root=os.path.join(path, "static"))

        run(host="0.0.0.0", port=8098, quiet=True)

    def prompt() -> None:
        from time import sleep

        print("请访问 http://localhost:8098 以编辑恩格玛机")

        items = ["|", "/", "—", "\\"]
        while not stop:
            for item in items:
                print("\r正在等待编辑完成 %s" % item, end="")
                sleep(0.2)

        print("\r" * 10 + "恩格玛机已编辑完毕", end="")

    t1 = threading.Thread(target=run, daemon=True)
    t2 = threading.Thread(target=prompt)

    t1.start()
    t2.start()

    while t2.is_alive():
        pass

    return
