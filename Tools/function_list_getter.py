# pylint: disable=[W,R,C]

import re


with open("./Engine/Resources/Functions.py", "r+", encoding="utf-8") as funcs:
    matches = re.findall(r"    id = Identifier\(\"([^\"]*)\", \"([^\"]*)\", \"([^\"]*)\"\)", funcs.read())
    print(matches)

out = ""

_a, _b = "", ""
for a, b, c in matches:
    a: str
    b: str
    c: str

    if "$" in b:
        continue

    if _a != a:
        out += f"# {a.title()}\n"
    if _b != b:
        out += f"## {b.title().strip('/')}\n"
    out += f"- {a}:{b}{c}\n"

    _a, _b = a, b
with open("./function_list.md", "w+", encoding="utf-8") as f:
    f.write(out)

