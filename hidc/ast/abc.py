from hidc.lexer import Span
from hidc.utils.data_abc import DataABC, Abstract

class Statement(DataABC):
    span: Abstract[Span]


class Block(Statement):
    pass


class Expression(Statement):
    pass


class Assignable(Expression):
    pass
