import sys
import argparse


"""
  Given a dict of accepted_arguments, builds options using argparse, if --use-samples is given, defaults will be used (good for testing).

  Example accepted_arguments:

  accepted_arguments = {
      "username": {"type": str, "sample_value": "james"},
      "hard_limit": {"type": int, "sample_value": 65535},
  }
"""


def fetch(accepted_arguments: dict) -> dict, str:
    gathered_args = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action=argparse.BooleanOptionalAction)
    parser.add_argument("--use-samples", action=argparse.BooleanOptionalAction)
    parser.add_argument(
        "--phase", action=argparse.BooleanOptionalAction, default="grade"
    )

    for k, v in accepted_arguments.items():
        parser.add_argument(f"--{k}", type=v["type"])

    args = parser.parse_args()

    if args.use_samples:
        for k, v in accepted_arguments.items():
            if vars(args)[k]:
                print(
                    "Conflict: cannot set accept arguments when --user-samples is set"
                )
                sys.exit(1)

            gathered_args = vars(args)
            gathered_args[k] = v["sample_value"]

    else:
        gathered_args = vars(args)

    del gathered_args["use_samples"]
    del gathered_args["phase"]

    return gathered_args, args.phase
