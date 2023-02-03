#coding:utf-8
"""帮助初学者写 Hello world!"""

import ctypes as _ctypes
import os as _os
import platform as _platform
import typing as _typing

__all__: list[str] = ["hello_world"]

if _os.name == "nt" and _platform.machine() == "AMD64":
    hello_world = getattr(
        _ctypes.WinDLL(_os.path.join(
            _os.path.split(_os.path.abspath(__file__))[0],
            "dll",
            "fxxkpy-dll.dll",
        )),
        "hello_world",
    )
else:
    hello_world = lambda: print("hello_world")

hello_world: _typing.Callable[[], None]
hello_world()

del _ctypes, _os, _platform, _typing
