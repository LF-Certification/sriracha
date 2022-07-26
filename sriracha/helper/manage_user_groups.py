import crypt
import grp
import pwd
import spwd
import subprocess
import sys

def is_user_exists(username):
    """Checks User existence"""
    try:
        pwd.getpwnam(username)
        return True
    except:  # pylint: disable=bare-except
        log.info("User someusr does not exist.")

    return False


def is_group_exists(groupname):
    """Checks group existence"""
    try:
        grp.getgrnam(groupname)
        return True
    except:  # pylint: disable=bare-except
        log.info("Group %s does not exist.", groupname)

    return False


def check_passwd(username, expected_passwd):
    """Checks user passwd"""
    try:
        password = spwd.getspnam(username).sp_pwdp
        return password == crypt.crypt(expected_passwd, password)
    except:  # pylint: disable=bare-except
        log.info("Failing to get passsword for the user %s", username)

    return False


def check_gid(groupname, expected_gid):
    """Checks groupid for groupname"""
    try:
        actual_gid = grp.getgrnam(groupname).gr_gid

        if actual_gid == int(expected_gid):
            return True
    except:  # pylint: disable=bare-except
        log.info("Failed to get group id for %s", groupname)

    return False


def user_exists_in_group(groupname, username):
    """Checks user existence in the group"""
    try:
        grp_mems = grp.getgrnam(groupname).gr_mem

        if username in grp_mems:
            return True
    except:  # pylint: disable=bare-except
        log.info("Faileed to get group members of the group %s", groupname)

    return False


def check_user_primary_grp(groupname, username):
    """Checks primary group of the user"""
    try:
        p_gid = pwd.getpwnam(username).pw_gid
        actual_grp_name = grp.getgrgid(p_gid).gr_name

        if actual_grp_name == groupname:
            return True
    except:  # pylint: disable=bare-except
        log.info("Failed to get user group of %s", groupname)

    return False


def check_non_interactive_shell(username):
    """Checks for non interactive shell of a user"""
    try:
        expected_shells = ["/bin/false", "/sbin/nologin"]
        actual_shell = pwd.getpwnam(username).pw_shell

        # Checking interactive login is effectively possible
        cmd = ["su", "-", username, "-c", "echo $-"]
        output = subprocess.run(
            cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        if actual_shell in expected_shells and output.returncode == 1:
            return True
    except:  # pylint: disable=bare-except
        log.info("Failed to get the user shell for %s", username)

    return False