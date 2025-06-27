import unittest
from io import StringIO
from unittest.mock import patch

from src.parser import Parser
from src.interpreter import Interpreter
from src.token import Token, TokenType


class TestInterpreter(unittest.TestCase):
    def test_arithmetic_operations(self):
        # print 1 + 2 * 3 - 4 / 2;
        tokens = [
            Token(TokenType.PRINT, "print", None, 1),
            Token(TokenType.NUMBER, "1", 1.0, 1),
            Token(TokenType.PLUS, "+", None, 1),
            Token(TokenType.NUMBER, "2", 2.0, 1),
            Token(TokenType.STAR, "*", None, 1),
            Token(TokenType.NUMBER, "3", 3.0, 1),
            Token(TokenType.MINUS, "-", None, 1),
            Token(TokenType.NUMBER, "4", 4.0, 1),
            Token(TokenType.SLASH, "/", None, 1),
            Token(TokenType.NUMBER, "2", 2.0, 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        parser = Parser(tokens)
        statements = parser.parse()
        interpreter = Interpreter()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            interpreter.interpret(statements)
            self.assertEqual(fake_out.getvalue().strip(), "5")

    def test_print_statement(self):
        # print "hello world";
        tokens = [
            Token(TokenType.PRINT, "print", None, 1),
            Token(TokenType.STRING, '"hello world"', "hello world", 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        parser = Parser(tokens)
        statements = parser.parse()
        interpreter = Interpreter()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            interpreter.interpret(statements)
            self.assertEqual(fake_out.getvalue().strip(), "hello world")

    def test_variable_assignment(self):
        # var a = 1; var b = 2; a = a + b; print a;
        tokens = [
            Token(TokenType.VAR, "var", None, 1),
            Token(TokenType.IDENTIFIER, "a", None, 1),
            Token(TokenType.EQUAL, "=", None, 1),
            Token(TokenType.NUMBER, "1", 1.0, 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.VAR, "var", None, 1),
            Token(TokenType.IDENTIFIER, "b", None, 1),
            Token(TokenType.EQUAL, "=", None, 1),
            Token(TokenType.NUMBER, "2", 2.0, 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.IDENTIFIER, "a", None, 1),
            Token(TokenType.EQUAL, "=", None, 1),
            Token(TokenType.IDENTIFIER, "a", None, 1),
            Token(TokenType.PLUS, "+", None, 1),
            Token(TokenType.IDENTIFIER, "b", None, 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.PRINT, "print", None, 1),
            Token(TokenType.IDENTIFIER, "a", None, 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        parser = Parser(tokens)
        statements = parser.parse()
        interpreter = Interpreter()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            interpreter.interpret(statements)
            self.assertEqual(fake_out.getvalue().strip(), "3")


if __name__ == "__main__":
    unittest.main()