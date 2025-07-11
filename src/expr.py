#####################################
# GENERATED BY tool/generate_ast.py #
#####################################

from abc import ABC, abstractmethod
from typing import TypeVar, override
from src import *


R = TypeVar("R")


class ExprVisitor[R](ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: "Assign") -> R: ...
    @abstractmethod
    def visit_binary_expr(self, expr: "Binary") -> R: ...
    @abstractmethod
    def visit_grouping_expr(self, expr: "Grouping") -> R: ...
    @abstractmethod
    def visit_literal_expr(self, expr: "Literal") -> R: ...
    @abstractmethod
    def visit_unary_expr(self, expr: "Unary") -> R: ...
    @abstractmethod
    def visit_variable_expr(self, expr: "Variable") -> R: ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor[R]) -> R: ...


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_literal_expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_unary_expr(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_variable_expr(self)
