import gzip, bz2
from pathlib import Path
import re

def gen_open(paths):
    for path in paths:
        if path.suffix == '.gz':
            yield gzip.open(path, 'rt')
        elif path.suffix == '.bz2':
            yield bz2.open(path, 'rt')
        else:
            yield open(path, 'rt')

def gen_cat(sources):
    for src in sources:
        yield from src

def gen_grep(pat, lines):
    patc = re.compile(pat)
    return (line for line in lines if patc.search(line))

def field_map(dictseq, name, func):
    for d in dictseq:
        d[name] = func(d[name])
        yield d 

def lines_from_dir(filepat, dirname):
    names = Path(dirname).rglob(filepat)
    files = gen_open(names)
    lines = gen_cat(files)
    return lines 

def apache_log(lines):
    groups = (logpat.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)
    colnames = ('host', 'referrer', 'user', 'datetime',
                'method', 'request', 'proto', 'status', 'bytes')
    log = (dict(zip(colnames, t)) for t in tuples)
    log = field_map(log, "bytes", lambda s: int(s) if s != '-' else 0)
    log = field_map(log, "status", int)
    return log


if __name__ == "__main__":
    logpats = r'(\S+) (\S+) (\S+) \[(.*?)\] '\
              r'"(\S+) (\S+) (\S+)" (\S+) (\S+)'
    logpat = re.compile(logpats)
    logdir = "/home/kuchi-chan/dbeaz/generators_1/"
    lines = lines_from_dir("access-log*", logdir)
    log = apache_log(lines)

    # Now we can make some queries...
    stat404 = {
        r['request'] for r in log if r['status'] == 404
    }
    
    large = (r for r in log if r['bytes'] > 1000000)
    for r in large:
        print(r['request'], r['bytes'])

    # Collect unique host IP Adresses
    hosts = {r['host'] for r in log}

    # Find the number of file downloads
    sum(1 for r in log if r['request'] == '/ply/ply-2.3.tar.gz')


    # Find who has been hitting robots.txt
    addrs = {r['host'] for r in log if 'robots.txt' in r['request']}

    import socket
    for addr in addrs:
        try:
            print(socket.gethostbyaddr(addr)[0])
        except socket.herror:
            print(addr)
