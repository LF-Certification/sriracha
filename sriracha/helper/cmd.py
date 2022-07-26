import subprocess

def exec_cmd(cmd):
    try:
        subprocess.run(cmd, check=True)
    except:  # pylint: disable=bare-except
        log.error("Failed to execute the command.")
        sys.exit(1)