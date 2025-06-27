
import unittest

from src.parser import Parser
from src.expr import Binary, Literal
from src.stmt import PrintStmt, ExpressionStmt, Var
from src.token import Token, TokenType


class TestParser(unittest.TestCase):
    def test_simple_expression(self):
        # 1 + 2;
        tokens = [
            Token(TokenType.NUMBER, "1", 1, 1),
            Token(TokenType.PLUS, "+", None, 1),
            Token(TokenType.NUMBER, "2", 2, 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        parser = Parser(tokens)
        statements = parser.parse()
        self.assertEqual(len(statements), 1)
        statement = statements[0]
        self.assertIsInstance(statement, ExpressionStmt)
        expression = statement.expression
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.PLUS)

    def test_variable_declaration(self):
        # var a = 1;
        tokens = [
            Token(TokenType.VAR, "var", None, 1),
            Token(TokenType.IDENTIFIER, "a", None, 1),
            Token(TokenType.EQUAL, "=", None, 1),
            Token(TokenType.NUMBER, "1", 1, 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        parser = Parser(tokens)
        statements = parser.parse()
        self.assertEqual(len(statements), 1)
        statement = statements[0]
        self.assertIsInstance(statement, Var)
        self.assertEqual(statement.name.lexeme, "a")
        self.assertIsInstance(statement.initializer, Literal)
        self.assertEqual(statement.initializer.value, 1)

    def test_print_statement(self):
        # print "hello";
        tokens = [
            Token(TokenType.PRINT, "print", None, 1),
            Token(TokenType.STRING, '"hello"', "hello", 1),
            Token(TokenType.SEMICOLON, ";", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ]
        parser = Parser(tokens)
        statements = parser.parse()
        self.assertEqual(len(statements), 1)
        statement = statements[0]
        self.assertIsInstance(statement, PrintStmt)
        self.assertIsInstance(statement.expression, Literal)
        self.assertEqual(statement.expression.value, "hello")


if __name__ == "__main__":
    unittest.main()
