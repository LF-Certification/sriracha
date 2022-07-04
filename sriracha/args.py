import sys
import argparse

"""
  Given a dict of accepted_arguments, builds options using argparse, if
  --use-samples is given, defaults will be used (good for testing).

  Example accepted_arguments:

  accepted_arguments = {
      "username": {"type": str, "sample_value": "james"},
      "hard_limit": {"type": int, "sample_value": 65535},
  }
"""


def fetch(accepted_arguments: dict) -> tuple:
    gathered_args = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action=argparse.BooleanOptionalAction)
    parser.add_argument("--use-samples", action=argparse.BooleanOptionalAction)
    parser.add_argument("--phase", default="setup", type=str)

    for k, v in accepted_arguments.items():
        parser.add_argument(f"--{k}", type=v["type"])

    args = parser.parse_args()

    gathered_args = vars(args)
    if args.use_samples:
        for k, v in accepted_arguments.items():
            if vars(args)[k]:
                print(
                    "Conflict: cannot set accept arguments when --user-samples is set"
                )
                sys.exit(1)

            gathered_args[k] = v["sample_value"]

    phase = gathered_args["phase"]

    del gathered_args["use_samples"]
    del gathered_args["phase"]

    return gathered_args, phase
