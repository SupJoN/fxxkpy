#coding:utf-8
"""帮助初学者写 Hello world!"""

import ctypes as __ctypes
import os as __os
import platform as __platform
import typing as __typing

__all__: list[str] = ["hello_world"]

if __os.name == "nt" and __platform.machine() == "AMD64":
    hello_world = getattr(
        __ctypes.WinDLL(__os.path.join(
            __os.path.split(__os.path.abspath(__file__))[0],
            "dll",
            "fxxkpy-dll.dll",
        )),
        "hello_world",
    )
else:
    hello_world = lambda: print("hello_world")

hello_world: __typing.Callable[[], None]
hello_world()

del __ctypes, __os, __platform, __typing
