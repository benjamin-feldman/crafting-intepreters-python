from src.token import Token


class Environment:
    def __init__(self):
        self._values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        self._values[name] = value

    def get(self, name: Token) -> object:
        from src.interpreter import LoxRuntimeError

        if name.lexeme in self._values:
            return self._values[name.lexeme]

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name: Token, value: object) -> None:
        from src.interpreter import LoxRuntimeError

        if name.lexeme in self._values:
            self._values[name.lexeme] = value
            return

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}.")
