import subprocess
import os
import re
import tempfile

lost_output_re = re.compile(r"^([a-z0-9_]+) ([a-z0-9.]+)$")

# matches the instruction read count in the first group, and the function name in the second group
# (for the callgrind and callgrind_annotate options specified below)
callgrind_annotate_re = re.compile(r"^\s*([0-9,]+)[^:]+:([^()]+)")

def maybe_to_num(s):
    try:
        n = float(s)
    except:
        return s
    return int(n) if n.is_integer() else n

def prepare_lost_args(args):
    return [os.getcwd() + '/lost', 'pipeline'] + list(map(str, args))

# Runs LOST with the given command-line parameters. Parses its output, returning a dictionary of
# everything that got printed from comparators and similar.
def run_lost(args):
    actual_args = prepare_lost_args(args)
    print('Running: ' + ' '.join(actual_args))
    proc = subprocess.run(actual_args,
                          check=False,
                          capture_output=True)
    print('Done, stderr: ' + proc.stderr.decode('ascii'))
    if proc.returncode != 0:
        raise RuntimeError('Nonzero exit code from LOST, %d' % proc.returncode)
    result = dict()
    for line in proc.stdout.decode('ascii').splitlines():
        matched = lost_output_re.match(line)
        if matched:
            result[matched.group(1)] = maybe_to_num(matched.group(2))
    return result

class LostDatabase:
    """
    Use this class via the `with` statement, eg `with LostDatabase(['--kvector', ...]) as db_path:`. The actual database won't be generated until __enter__, so in fact it can /only/ be used via the `with` statement.
    """

    def __init__(self, cli_args):
        self.cli_args = cli_args

    def __enter__(self):
        fd, self.db_path = tempfile.mkstemp()
        os.close(fd)
        stringy_args = ['database'] + list(map(str, self.cli_args)) + ['--output', self.db_path]
        print('Creating database: lost ' + ' '.join(stringy_args), flush=True)
        subprocess.run([os.getcwd() + '/lost'] + stringy_args,
                       check=True)
        return self.db_path
    def __exit__(self, *args):
        if self.db_path:
            os.unlink(self.db_path)

def run_callgrind_on_lost(args):
    try:
        fd, callgrind_out_file = tempfile.mkstemp()
        os.close(fd)
        actual_args = ['valgrind', '--tool=callgrind', '--callgrind-out-file=' + callgrind_out_file] + prepare_lost_args(args)
        print('Running (callgrind): ' + ' '.join(actual_args))
        proc = subprocess.run(actual_args,
                              check=True,
                              capture_output=True)
        print('Done (callgrind), sending to callgrind_annotate')
        # Run callgrind_analyze on proc.stdout
        analyze_proc = subprocess.run(['callgrind_annotate', '--auto=no', '--context=0', '--inclusive=yes', '--threshold=100',
                                       callgrind_out_file],
                                      input=proc.stdout,
                                      check=True,
                                      capture_output=True)

        # Parse output into hashmap from fns to counts. Use the first instance of a function name when it occurs multiple times
        result = {}
        for line in analyze_proc.stdout.decode('utf-8').splitlines():
            match = callgrind_annotate_re.match(line)
            if match and not match.group(2) in result:
                    result[match.group(2)] = int(match.group(1).replace(',', ''))
        return result

    finally:
        if callgrind_out_file:
            os.remove(callgrind_out_file)
