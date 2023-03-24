import subprocess
import os
import re
import tempfile

lost_output_re = re.compile(r"^([a-z0-9_]+) ([a-z0-9.]+)$")

def maybe_to_num(s):
    try:
        n = float(s)
    except:
        return s
    return int(n) if n.is_integer() else n

# Runs LOST with the given command-line parameters. Parses its output, returning a dictionary of
# everything that got printed from comparators and similar.
def run_lost(args):
    stringy_args = ['pipeline'] + list(map(str, args))
    print('Running: lost ' + ' '.join(stringy_args), flush=True)
    proc = subprocess.run([os.getcwd() + '/lost'] + stringy_args,
                          check=True, # throw an error if nonzero exit code
                          capture_output=True)
    print('Done, stderr: ' + str(proc.stderr.decode('ascii')))
    result = dict()
    for line in proc.stdout.decode('ascii').splitlines():
        matched = lost_output_re.match(line)
        if matched:
            result[matched.group(1)] = maybe_to_num(matched.group(2))
    return result

class LostDatabase:
    """
    Use this class via the `with` statement, eg `with LostDatabase(['--kvector', ...]) as db_path:`, then the database will automatically be deleted when you're done!
    """

    def __init__(self, cli_args):
        fd, self.db_path = tempfile.mkstemp()
        os.close(fd)
        stringy_args = ['database'] + list(map(str, cli_args)) + ['--output', self.db_path]
        print('Creating database: lost ' + ' '.join(stringy_args), flush=True)
        subprocess.run([os.getcwd() + '/lost'] + stringy_args,
                       check=True)

    def __enter__(self):
        return self.db_path
    def __exit__(self, *args):
        os.unlink(self.db_path)
