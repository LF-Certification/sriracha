import json

global CHECK_RESULTS
CHECK_RESULTS = {}

# This decorator should be used to decorate all checks.
def check(func):
    def inner(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        function_name = func.__name__
        globals()["CHECK_RESULTS"][function_name] = returned_value
        return returned_value

    return inner


def get_score_report():
    check_results = globals()["CHECK_RESULTS"]
    checks_executed: int = len(check_results.keys())
    checks_passed: int = 0
    checks_successful = []
    checks_failed = []

    for name, result in check_results.items():
        if result:
            checks_passed += 1
            checks_successful.append(name)
            continue

        checks_failed.append(name)

    return {
        "checks_executed": checks_executed,
        "checks_passed": checks_passed,
        "checks_successful": checks_successful,
        "checks_failed": checks_failed,
        "output_version": 1,
    }


def report_score():
    print(json.dumps(get_score_report()))
