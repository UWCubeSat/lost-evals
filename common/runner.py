import subprocess
import os
import re
import tempfile
import socket
from time import sleep

lost_output_re = re.compile(r"^([a-z0-9_]+) ([a-z0-9.-]+)$")

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

def run_openstartracker_calibrate(testdir):
    # Call calibrate.py testdir
    print('Running calibrate.py %s' % testdir)
    proc = subprocess.run(['python3', 'calibrate.py', testdir],
                          check=True)
    print('Done calibrating, methinks')

def start_openstartracker_server(testdir):
    """Start the server, returning the process which should be terminated when appropriate"""
    # Run startracker.py testdir/calibration.txt 2023 testdir/median_image.png
    print('Running startracker.py %s/calibration.txt 2023 %s/median_image.png' % (testdir, testdir))
    proc = subprocess.Popen(['python3', 'startracker.py', testdir + '/calibration.txt', '2023', testdir + '/median_image.png'],
                            stderr=subprocess.PIPE)
    sleep(5)
    print('Server online!')
    # os.set_blocking(proc.stderr.fileno(), False) # supposedly this makes readline nonblocking
    return proc

def solve_openstartracker(image, proc):
    # Send `rgb.solve_image('image')` to the server
    print('Solving %s with openstartracker' % image)
    # Just send the text to 127.0.0.1:8010 over TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8010))
    s.sendall(("rgb.solve_image('%s')\n" % image).encode('ascii'))
    sleep(0.5);
    s.close()
    # Read lines from proc
    times = []
    dec = None
    ra = None
    roll = None
    loops = 0
    while True:
        line = proc.stderr.readline().decode('ascii')
        if not line:
            raise RuntimeError('Server output ended too early!')
        if line.startswith('Time'):
            if line[5] != str(len(times)+1):
                raise RuntimeError('Server `Time` output out of order!')
            # strip line ending: this will only work on unix
            times.append(float(line[7:-1]))
            if line[5] == '6':
                break

        if line.startswith('DEC='):
            assert dec is None
            dec = float(line[4:-1])
        if line.startswith('RA='):
            assert ra is None
            assert dec is not None
            ra = float(line[3:-1])
        if line.startswith('ORIENTATION='):
            assert roll is None
            assert dec is not None
            assert ra is not None
            roll = float(line[12:-1])

        loops += 1
        if loops > 1000:
            raise RuntimeError('Server output too long!')

        # There are some random lines that don't start with any of these things that we would like to ignore. As well as empty lines.

    return times, dec, ra, roll

def stop_openstartracker(proc):
    proc.terminate()
    proc.wait()
