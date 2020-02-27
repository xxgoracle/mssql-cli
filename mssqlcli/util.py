import os
import subprocess

def encode(s):
    try:
        return s.encode('utf-8')
    except (AttributeError, SyntaxError):
        pass
    return s

# In Python 3, all strings are sequences of Unicode characters.
# There is a bytes type that holds raw bytes.
# In Python 2, a string may be of type str or of type unicode.
def decode(s):
    try:
        return s.decode('utf-8')
    except (AttributeError, SyntaxError, UnicodeEncodeError):
        pass
    return s

def is_command_valid(command):
    """
    Checks if command is recognized on machine. Used to determine installations
    of 'less' pager.
    """
    if not command:
        return False

    # We import `DEVNULL` to create silent calls from subprocess. Python 3 uses
    # `DEVNULL` from subprocess while Python 2 uses os.
    try:
        from subprocess import DEVNULL  # Python 3.
    except ImportError:
        DEVNULL = open(os.devnull, 'wb')

    try:
        # call command silentyly
        subprocess.call(command, stdout=DEVNULL, stderr=DEVNULL)
    except OSError:
        return False
    else:
        return True
