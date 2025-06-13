from typing import override
from expr import ExprVisitor, Expr
from src.expr import Binary, Grouping, Literal, Unary


class AstPrinter(ExprVisitor[str]):
    def print(self, expr: Expr):
        return expr.accept(self)

    @override
    def visit_binary_expr(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @override
    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    @override
    def visit_literal_expr(self, expr: Literal) -> str:
        if not expr.value:
            return "nil"
        return str(expr.value)

    @override
    def visit_unary_expr(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        res = "("
        res += name
        for expr in exprs:
            res += " "
            res += expr.accept(self)

        res += ")"

        return res


if __name__ == "__main__":
    from src.token import Token, TokenType
    from src.expr import Binary, Unary, Literal, Grouping

    expression = Binary(
        left=Unary(operator=Token(TokenType.MINUS, "-", None, 1), right=Literal(123)),
        operator=Token(TokenType.STAR, "*", None, 1),
        right=Grouping(expression=Literal(45.67)),
    )

    printer = AstPrinter()
    print(printer.print(expression))
