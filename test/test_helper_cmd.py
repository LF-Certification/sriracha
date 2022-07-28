from src.sriracha.helper import cmd


def test_answer():
    assert cmd.exec_cmd("echo hello").stdout == b"hello\n"
