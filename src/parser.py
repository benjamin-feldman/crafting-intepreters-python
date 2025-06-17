from src.token import Token, TokenType
from src.expr import Expr, Binary, Unary, Grouping, Literal
from src.stmt import Stmt, PrintStmt, ExpressionStmt


class ParseError(Exception): ...


class Parser:
    """
    Implements the Lox grammar:
    program        -> declaration* EOF ;
    declaration    -> varDecl
                    | statement ;
    statement      -> exprStmt
                    | printStmt ;
    exprStmt       -> expression ";" ;
    printStmt      -> "print" expression ";" ;
    varDecl        -> "var" IDENTIFIER ( "=" expression )? ";" ;
    expression     -> equality ;
    equality       -> comparison ( ( "!=" | "==" ) comparison )* ;
    comparison     -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    term           -> factor ( ( "-" | "+" ) factor )* ;
    factor         -> unary ( ( "/" | "*" ) unary )* ;
    unary          -> ( "!" | "-" ) unary
                    | primary ;
    primary        -> NUMBER
                    | STRING
                    | "true"
                    | "false"
                    | "nil"
                    | "(" expression ")"
                    | IDENTIFIER ;
    """

    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._current = 0

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self._is_at_end:
            statements.append(self._statement())
        return statements

    def _statement(self) -> Stmt:
        if self._match(TokenType.PRINT):
            return self._print_statement()
        return self._expression_statement()

    def _print_statement(self) -> PrintStmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def _expression_statement(self) -> ExpressionStmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return ExpressionStmt(value)

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        expr = self._term()

        while self._match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)

        return expr

    def _term(self) -> Expr:
        expr = self._factor()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)

        return expr

    def _factor(self) -> Expr:
        expr = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            expr = Unary(operator, right)
        else:
            expr = self._primary()

        return expr

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            literal = self._previous().literal
            return Literal(literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()

        raise self._error(self._peek(), message)

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end:
            return False
        return self._peek().type == token_type

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _advance(self) -> Token:
        if not self._is_at_end:
            self._current += 1
        return self._previous()

    @property
    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _error(self, token: Token, message: str) -> ParseError:
        from src.lox import Lox

        Lox.token_error(token, message)

        return ParseError()

    def _synchronize(self) -> None:
        self._advance()

        while not self._is_at_end:
            if self._previous().type == TokenType.SEMICOLON:
                return

            match self._peek().type:
                case TokenType.CLASS:
                    pass
                case TokenType.FUN:
                    pass
                case TokenType.VAR:
                    pass
                case TokenType.FOR:
                    pass
                case TokenType.IF:
                    pass
                case TokenType.WHILE:
                    pass
                case TokenType.PRINT:
                    pass
                case TokenType.RETURN:
                    return
                case _:
                    pass
