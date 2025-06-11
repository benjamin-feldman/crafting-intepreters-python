import argparse
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.scanner import Scanner


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

    @staticmethod
    def _run(source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

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
    def _report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        cls.had_error = True


if __name__ == "__main__":
    lox = Lox()
    lox.main()
