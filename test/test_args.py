import pytest

from sriracha import args


def test_fetch():
    accepted_arguments = {
        "username": {"type": str, "sample_value": "james"},
        "hard_limit": {"type": int, "sample_value": 65535},
    }

    import sys

    sys.argv.append("--use-samples")
    sys.argv.append("--debug")
    fetched_args, phase = args.fetch(accepted_arguments)

    assert 65535 == fetched_args["hard_limit"]
    assert "james" == fetched_args["username"]
    assert True == fetched_args["debug"]
