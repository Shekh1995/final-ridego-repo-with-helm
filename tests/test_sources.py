import ast
from pathlib import Path
ROOT=Path(__file__).parents[1]
def test_python_sources_compile():
    for p in (ROOT/"services").glob("*/app.py"): ast.parse(p.read_text())
