import readline
import atexit
import os


HIST_LENGTH = 1000


def enable_history(file='~/.local/rpncalc-history'):

    hist_file = os.path.expanduser(file)
    try:
        readline.read_history_file(hist_file)
    except FileNotFoundError:
        print(
            f"No history file found at {file}."
            f" Create empty file with 'touch {file}"
            " to enable this feature"
            )
        # No file, return
        return
    except PermissionError:
        print(f"Permissions error on history file {hist_file}")
        # Return to avoid atexit register of write
        return

    readline.set_history_length(HIST_LENGTH)

    # Write to history on app close
    # Consider rewriting with readline.append_history_file
    # to allow for concurrent interactive sessions
    atexit.register(readline.write_history_file, hist_file)
