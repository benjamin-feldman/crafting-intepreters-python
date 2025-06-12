import argparse
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.scanner import Scanner
from src.token import Token, TokenType
from src.parser import Parser
from src.ast_printer import AstPrinter


class Lox:
    had_error: bool = False

    def main(self):
        parser = argparse.ArgumentParser(description="Usage: plox [script]")
        parser.add_argument("script", nargs="?", help="The script file to run")
        args = parser.parse_args()
        script_filepath = args.script

        if script_filepath:
            self._run_file(script_filepath)
        else:
            self._run_prompt()

    def _run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expr = parser.parse()

        if self.had_error or (not expr):
            return

        print(AstPrinter().print(expr))

    def _run_file(self, filepath: str):
        with open(filepath, mode="r", encoding="utf-8") as source:
            self._run(source.read())

        if self.had_error:
            sys.exit(65)

    def _run_prompt(self):
        while True:
            print("> ", end="")
            line = input()
            if not line:
                break
            self._run(line)

            self.had_error = False

    @classmethod
    def error(cls, line: int, message: str):
        cls._report(line, "", message)

    @classmethod
    def token_error(cls, token: Token, message: str):
        if token.type == TokenType.EOF:
            cls._report(token.line, " at end", message)
        else:
            cls._report(token.line, " at '" + token.lexeme + "'", message)

    @classmethod
    def _report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        cls.had_error = True


if __name__ == "__main__":
    lox = Lox()
    lox.main()
