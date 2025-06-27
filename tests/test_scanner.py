
import unittest

from src.scanner import Scanner
from src.token import Token, TokenType


class TestScanner(unittest.TestCase):
    def test_single_tokens(self):
        source = "(){},.-+;*"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        expected_tokens = [
            Token(TokenType.LEFT_PAREN, "(", None, 1),
            Token(TokenType.RIGHT_PAREN, ")", None, 1),
            Token(TokenType.LEFT_BRACE, "{", None, 1),
            Token(TokenType.RIGHT_BRACE, "}", None, 1),
            Token(TokenType.COMMA, ",", None, 1),
            Token(TokenType.DOT, ".", None, 1),
            Token(TokenType.MINUS, "-", None, 1),
            Token(TokenType.PLUS, "+", None, 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.STAR, "*", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        self.assertEqual(len(tokens), len(expected_tokens))
        for i, token in enumerate(tokens):
            self.assertEqual(token.type, expected_tokens[i].type)
            self.assertEqual(token.lexeme, expected_tokens[i].lexeme)
            self.assertEqual(token.literal, expected_tokens[i].literal)
            self.assertEqual(token.line, expected_tokens[i].line)

    def test_operators(self):
        source = "! != = == > >= < <="
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        expected_tokens = [
            Token(TokenType.BANG, "!", None, 1),
            Token(TokenType.BANG_EQUAL, "!=", None, 1),
            Token(TokenType.EQUAL, "=", None, 1),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Token(TokenType.GREATER, ">", None, 1),
            Token(TokenType.GREATER_EQUAL, ">=", None, 1),
            Token(TokenType.LESS, "<", None, 1),
            Token(TokenType.LESS_EQUAL, "<=", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        self.assertEqual(len(tokens), len(expected_tokens))
        for i, token in enumerate(tokens):
            self.assertEqual(token.type, expected_tokens[i].type)
            self.assertEqual(token.lexeme, expected_tokens[i].lexeme)
            self.assertEqual(token.literal, expected_tokens[i].literal)
            self.assertEqual(token.line, expected_tokens[i].line)

    def test_string(self):
        source = '"hello world"'
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        expected_tokens = [
            Token(TokenType.STRING, '"hello world"', "hello world", 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        self.assertEqual(len(tokens), len(expected_tokens))
        for i, token in enumerate(tokens):
            self.assertEqual(token.type, expected_tokens[i].type)
            self.assertEqual(token.lexeme, expected_tokens[i].lexeme)
            self.assertEqual(token.literal, expected_tokens[i].literal)
            self.assertEqual(token.line, expected_tokens[i].line)

    def test_number(self):
        source = "123 123.456"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        expected_tokens = [
            Token(TokenType.NUMBER, "123", 123.0, 1),
            Token(TokenType.NUMBER, "123.456", 123.456, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        self.assertEqual(len(tokens), len(expected_tokens))
        for i, token in enumerate(tokens):
            self.assertEqual(token.type, expected_tokens[i].type)
            self.assertEqual(token.lexeme, expected_tokens[i].lexeme)
            self.assertEqual(token.literal, expected_tokens[i].literal)
            self.assertEqual(token.line, expected_tokens[i].line)

    def test_identifiers(self):
        source = "foo for var"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        expected_tokens = [
            Token(TokenType.IDENTIFIER, "foo", None, 1),
            Token(TokenType.FOR, "for", None, 1),
            Token(TokenType.VAR, "var", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        self.assertEqual(len(tokens), len(expected_tokens))
        for i, token in enumerate(tokens):
            self.assertEqual(token.type, expected_tokens[i].type)
            self.assertEqual(token.lexeme, expected_tokens[i].lexeme)
            self.assertEqual(token.literal, expected_tokens[i].literal)
            self.assertEqual(token.line, expected_tokens[i].line)


if __name__ == "__main__":
    unittest.main()
