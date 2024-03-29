import subprocess
import os
import pwd


def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)

    return result


def exec_cmd(command: str, user: str = "", check=True) -> subprocess.CompletedProcess:
    """Executes commands on behalf of uids

    :check: Toggle the "check" behavior or subprocess.run, raises error on non-zero return code.
    :returns:

    """
    # Run the command as the specified user.
    if user:
        # get user info from username
        pw_record = pwd.getpwnam(user)
        homedir = pw_record.pw_dir
        user_uid = pw_record.pw_uid
        user_gid = pw_record.pw_gid
        env = os.environ.copy()
        env.update({"HOME": homedir, "LOGNAME": user, "PWD": os.getcwd(), "USER": user})
        proc = subprocess.run(
            [command],
            shell=True,
            env=env,
            check=check,
            preexec_fn=demote(user_uid, user_gid),
            stdout=subprocess.PIPE,
        )
    else:
        proc = subprocess.run(
            [command], shell=True, stdout=subprocess.PIPE, check=check
        )

    return proc
