import crypt
import grp
import pwd
import spwd
import subprocess
import sys

def user_exists(username):
    """Checks User existence"""
    try:
        pwd.getpwnam(username)
        return True
    except KeyError as e:
        log.info("User someusr does not exist.")

    return False


def group_exists(groupname):
    """Checks group existence"""
    try:
        grp.getgrnam(groupname)
        return True
    except KeyError as e:
        log.info("Group %s does not exist.", groupname)

    return False


def check_passwd(username, expected_passwd):
    """Checks user passwd"""
    try:
        password = spwd.getspnam(username).sp_pwdp
        return password == crypt.crypt(expected_passwd, password)
    except KeyError as e:
        log.info("Failing to get passsword for the user %s", username)

    return False


def groupname_equals_gid(groupname, expected_gid):
    """Checks groupid for groupname"""
    actual_gid = None
    try:
        actual_gid = grp.getgrnam(groupname).gr_gid
    except KeyError as e:
        log.info("Failed to get group id for %s", groupname)

    if actual_gid == int(expected_gid):
            return True

    return False


def user_in_group(groupname, username):
    """Checks user existence in the group"""
    grp_mems = None
    try:
        grp_mems = grp.getgrnam(groupname).gr_mem
    except KeyError as e:
        log.info("Failed to get group members of the group %s", groupname)

    if username in grp_mems:
        return True
    return False


def check_user_primary_group(groupname, username):
    """Checks primary group of the user"""
    p_gid = None
    actual_grp_name = None
    try:
        p_gid = pwd.getpwnam(username).pw_gid
        actual_grp_name = grp.getgrgid(p_gid).gr_name

    except KeyError as e:
        log.info("Failed to get user group of %s", groupname)

    if actual_grp_name == groupname:
        return True

    return False


def user_shell_is_not_interactive(username):
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
