import subprocess
import os
import re

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
    print('Running lost ' + ' '.join(stringy_args), flush=True)
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
