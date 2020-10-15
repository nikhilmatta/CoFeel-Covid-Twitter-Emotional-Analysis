#!/usr/bin/env python3

#
# Parts of code taken from stackoverflow
#

import gzip
import json
import requests

from tqdm import tqdm
from twarc import Twarc
from pathlib import Path

twarc = Twarc()

url = "https://drive.google.com/file/d/1COJ1zrJE-acz0yZssIljRSAPyIRtS2EC/view?usp=sharing"
r = requests.get(url)

def reader_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def raw_newline_count(fname):
    f = open(fname, 'rb')
    f_gen = reader_generator(f.raw.read)
    return sum(buf.count(b'\n') for buf in f_gen)


if __name__ == "__main__":
    gzip_path = r.with_suffix('.jsonl.gz')
    if gzip_path.is_file():
        return

    num_ids = raw_newline_count(r)

    with gzip.open(gzip_path, 'w') as output:
        with tqdm(total=num_ids) as pbar:
            for tweet in twarc.hydrate(r.open()):
                output.write(json.dumps(tweet).encode('utf8') + b"\n")
                pbar.update(1)
