# coding:utf-8
def lowercase_a() -> None:
    data = "\x83ÑÓÊÏÕ\x89ÄÉÓ\x89蓬飱\x8a\x8a\x83\x8d\x81Ü\x83蓬飱\x83\x9b\x81\x9a\x98Þ"
    exec(*eval("".join((chr(ord(char) - 97) for char in data))))
