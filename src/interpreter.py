from typing import override

from src.expr import (
    Assign,
    Binary,
    Grouping,
    Literal,
    Expr,
    Unary,
    ExprVisitor,
    Variable,
)
from src.token import Token, TokenType
from src.stmt import StmtVisitor, Stmt, PrintStmt, ExpressionStmt, Var
from src.environment import Environment


class LoxRuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token


class Interpreter(ExprVisitor[object], StmtVisitor[None]):
    def __init__(self):
        self._environment = Environment()

    def interpret(self, statements: list[Stmt | None]) -> None:
        try:
            for statement in statements:
                self._execute(statement)
        except LoxRuntimeError as e:
            from src.lox import Lox

            Lox.runtime_error(e)

    @override
    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

    @override
    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self._evaluate(expr.expression)

    @override
    def visit_unary_expr(self, expr: Unary) -> object:
        right = self._evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self._check_number_operand(expr.operator, right)
                return -right  # type: ignore ; the cast might fail at runtime
            case TokenType.BANG:
                return not self._is_truthy(right)
            case _:
                return None

    @override
    def visit_binary_expr(self, expr: Binary) -> object:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        match expr.operator.type:
            case TokenType.STAR:
                return left * right  # type: ignore
            case TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                return left - right  # type: ignore
            case TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                return left / right  # type: ignore
            case TokenType.PLUS:
                self._check_number_string_operands(expr.operator, left, right)
                return left + right  # type: ignore
            case TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                return left > right  # type: ignore
            case TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return left >= right  # type: ignore
            case TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                return left < right  # type: ignore
            case TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return left <= right  # type: ignore
            case TokenType.EQUAL_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return self._is_equal(left, right)  # type: ignore
            case TokenType.BANG_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return not self._is_equal(left, right)  # type: ignore
            case _:
                return None

    @override
    def visit_printstmt_stmt(self, stmt: PrintStmt) -> None:
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))
        return None

    @override
    def visit_expressionstmt_stmt(self, stmt: ExpressionStmt) -> None:
        self._evaluate(stmt.expression)
        return None

    @override
    def visit_var_stmt(self, stmt: Var) -> None:
        value: object = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self._environment.define(stmt.name.lexeme, value)
        return None

    @override
    def visit_variable_expr(self, expr: Variable) -> object:
        return self._environment.get(expr.name)

    def _execute(self, stmt: Stmt | None) -> None:
        if stmt is not None:
            stmt.accept(self)

    @override
    def visit_assign_expr(self, expr: Assign) -> object:
        value = self._evaluate(expr.value)
        self._environment.assign(expr.name, value)
        return value

    def _evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def _is_truthy(self, obj: object) -> bool:
        # In Lox everything is truthy, except from nil and false
        if not obj:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def _is_equal(self, a: object, b: object) -> bool:
        if not a and not b:
            return True
        if not a:
            return False
        return a == b

    def _check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(
        self, operator: Token, left: object, right: object
    ) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def _check_number_string_operands(
        self, operator: Token, left: object, right: object
    ) -> None:
        if (isinstance(left, float) and isinstance(right, float)) or (
            isinstance(left, str) and isinstance(right, str)
        ):
            return
        raise LoxRuntimeError(operator, "Operands must be two numbers or two strings.")

    def _stringify(self, obj: object) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        if isinstance(obj, bool):
            if obj:
                return "true"
            return "false"
        return str(obj)
