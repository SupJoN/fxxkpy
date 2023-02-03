# coding: utf-8
import ast
import inspect
import itertools
from types import CodeType, FunctionType
from typing import Any, cast

try:
    from rich import print
except Exception:
    pass

__all__ = ("HE", )


class RemoveHeDecorator(ast.NodeTransformer):
    """
    移除 `@he` 装饰器，否则会陷入无穷递归
    """
    def __init__(self, fun_name: str):
        self.fun_name: str = fun_name

    def _is_he_deco(self, expr: Any) -> bool:
        return not (isinstance(expr, ast.Name) and expr.id == "he")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """
        从顶级函数的定义里移除 `@he`
        """
        if node.name == self.fun_name:
            node.decorator_list: list = [expr for expr in node.decorator_list if self._is_he_deco(expr)]
        return node


class UnwrapHeBitOr(ast.NodeVisitor):
    """
    展开 `|` 运算
    """
    def __init__(self) -> None:
        self.exprs: list[ast.expr] = []

    def visit_Call(self, node: ast.Call) -> ast.Call:
        """
        嵌套的函数调用，不展开内层调用的 `|` 运算
        """
        return node

    def visit_BinOp(self, node: ast.BinOp) -> bool:
        """
        递归并 on-the-fly 地把找到的表达式压入 `self.exprs`

        返回值表示该 AST 结点是否——包含 `|` 且已压入 `self.exprs`
        """
        if isinstance(node.op, ast.BitOr):
            if isinstance(node.left, ast.BinOp) and self.visit_BinOp(node.left):  # 遍历左侧即可
                self.exprs.append(node.right)
                return True
            else:
                self.exprs.extend((node.left, node.right))
                return True
        else:
            return False


class RewriteHeCallStmt(ast.NodeTransformer):
    """
    展开函数调用语句
    """
    def _unwrap_arg(self, arg: ast.expr) -> list:
        """
        展开一个实参 `expr`
        """
        binary: UnwrapHeBitOr = UnwrapHeBitOr()
        binary.visit(arg)
        return binary.exprs if len(binary.exprs) else [arg]

    def visit_Expr(self, node: ast.Expr) -> (ast.Expr | list):
        """
        只有函数调用语句（`Expr -> Call`）可以被展开
        """
        if isinstance(node.value, ast.Call):
            call: ast.Call = node.value
            prod: itertools.product = itertools.product(*[self._unwrap_arg(arg) for arg in call.args])
            # 笛卡尔积

            return [ast.Expr(ast.Call(func=call.func, args=list(pair), keywords=call.keywords)) for pair in prod]
        return node


def he(f: FunctionType, SHOULD_DUMP_RESULT: bool = False) -> FunctionType:
    src: str = inspect.getsource(f)
    # 通过反射直接从对象拿到源代码字符串

    tree: ast.Module = ast.parse(src)  # 生成 AST
    result: ast.Module = ast.fix_missing_locations(RewriteHeCallStmt().visit(RemoveHeDecorator(f.__name__).visit(tree)))

    if SHOULD_DUMP_RESULT:
        print(ast.unparse(result))

    code: CodeType = compile(result, "<string>", "exec")  # 编译为字节码
    if SHOULD_DUMP_RESULT:
        print(code.co_consts, code.__class__)
    v: FunctionType = FunctionType(code.co_consts[0], f.__globals__, f.__name__)
    return cast(FunctionType, v)


class HE(object):
    '''
    HE
    ==

    作者
    ----
        原作者: tomyxw

        原视频: https://b23.tv/6oJiAGR

        完善自 SupJoN

    注意
    ----
        将 SHOULD_DUMP_RESULT 修改成 ```True``` 可以打印结果

    例子
    ----
    ```python
    from fxxkpy import HE

    def forceCon(whichKey, force):
        print(f"forceCon({whichKey}, {force})")


    @HE
    def littleFingerForce():
        forceCon(1 | 2 | 6 | 7 | 11 | 52 | 57 | 58 | 65, 10)

    littleFingerForce()
    ```
    '''

    SHOULD_DUMP_RESULT: bool = False

    def __new__(cls, f: FunctionType) -> FunctionType:
        return he(f, cls.SHOULD_DUMP_RESULT)  # 返回 he 装饰的结果
