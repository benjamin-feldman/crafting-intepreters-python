from src.token import Token, TokenType


class Scanner:
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._tokens: list[Token] = []
        self._start: int = 0
        self._current: int = 0
        self._line: int = 1
        self._keywords: dict[str, TokenType] = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end:
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _scan_token(self):
        c = self._advance()
        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case "/":
                if self._match("/"):
                    while self._peek() != "\n" and not self._is_at_end:
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self._line += 1
            case '"':
                self._string()

            case _:
                if c.isdigit():
                    self._number()
                elif self._is_alpha(c):
                    self._identifier()
                else:
                    from lox import Lox

                    # TODO: add a separated error handler, to avoid circular/lazy imports
                    Lox.error(self._line, f"Unexpected character: {c}.")

    def _advance(self) -> str:
        c = self._source[self._current]
        self._current += 1
        return c

    def _match(self, expected: str) -> bool:
        if self._is_at_end:
            return False
        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end:
            return "\0"
        return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return "\0"
        return self._source[self._current + 1]

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end:
            if self._peek() == "\n":
                self._line += 1
            self._advance()

        if self._is_at_end:
            from lox import Lox

            Lox.error(self._line, "Unterminated string.")

        self._advance()

        value = self._source[self._start + 1 : self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        if self._peek() and self._peek_next().isdigit():
            self._advance()

        while self._peek().isdigit():
            self._advance()

        self._add_token(
            TokenType.NUMBER, float(self._source[self._start : self._current])
        )

    def _identifier(self) -> None:
        while self._is_alphanumeric(self._peek()):
            self._advance()

        value = self._source[self._start : self._current]
        token_type: TokenType = self._keywords.get(value, TokenType.IDENTIFIER)
        self._add_token(token_type)

    def _add_token(self, type: TokenType, literal: object | None = None):
        text = self._source[self._start : self._current]
        self._tokens.append(Token(type, text, literal, self._line))

    def _is_alpha(self, char: str) -> bool:
        return char.isalpha() or char == "_"

    def _is_alphanumeric(self, char: str) -> bool:
        return char.isdigit() or self._is_alpha(char)

    @property
    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)
