from abc import abstractmethod, ABC
import os


def define_ast(output_dir: str, base_name: str, base_class_name: str, types: list[str]):
    os.makedirs(output_dir, exist_ok=True)

    path = f"{output_dir}/{base_name}.py"
    print(path)

    with open(path, "w") as f:
        f.write("from abc import ABC\n")
        f.write("from src import *\n")
        f.writelines("\n\n")
        f.write(f"class {base_class_name}(ABC):\n")
        f.write(f"\t...\n")
        f.write(f"\n")

        for t in types:
            class_name = t.split("=")[0].strip()
            fields = t.split("=")[1].strip()
            f.write(f"class {class_name}({base_class_name}):\n")
            f.write(f"\tdef __init__(self, {fields}):\n")
            field_list = fields.split(",")
            for field in field_list:
                field_name = field.split(":")[0].strip()
                f.write(f"\t\tself.{field_name} = {field_name}\n")
            f.write("\n\n")


if __name__ == "__main__":
    types = [
        "Binary   = left: Expr, operator: Token, right: Expr",
        "Grouping = expression: Expr",
        "Literal  = value: object",
        "Unary    = operator: Token, right: Expr",
    ]
    define_ast("src", "expr", "Expr", types)
