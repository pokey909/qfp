#!/usr/bin/env python
# -*- coding: utf_8 -*-

from qfp import ReferenceFingerprint
from qfp.db import QfpDB
import fnmatch
import os
import sqlite3
import multiprocessing as mp
from contextlib import closing
import sys

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts)]


def fingerprint(filenames):
    db = QfpDB()
    with sqlite3.connect('qfp.db') as conn:
        conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
        c = conn.cursor()
        for name in filenames:
            title = os.path.basename(name)
            print(name)
            # if not db._record_exists(c, title) and "thn010-04-sebastian_redenz_-_illusion" not in title:
            if not db._record_exists(c, title) in name:
                print("[" + str(os.getpid()) + "] Fingerprinting " + name)
                fp_r = ReferenceFingerprint(name)
                fp_r.create()
                db.store(fp_r, title)
            else:
                # print("[" + str(os.getpid()) + "] Fingerprint for " + name + " already exists. Skipping...")
                pass


def fingerprint_noStore((name, db_path)):
    db = QfpDB(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
        c = conn.cursor()
        title = os.path.basename(name)
        if not db._record_exists(c, title) and "thn010-04-sebastian_redenz_-_illusion" not in title:
            print("[" + str(os.getpid()) + "] Fingerprinting " + name)
            fp_r = ReferenceFingerprint(name)
            fp_r.create()
            return fp_r, title
        else:
            # print("[" + str(os.getpid()) + "] Fingerprint for " + name + " already exists. Skipping...")
            pass
        return None, ""


def createFingerprintsSerial(data_dir):
    matches = []
    for root, dirnames, filenames in os.walk(data_dir):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            fullname = os.path.join(root, filename)
            matches.append(fullname)

    fingerprint(matches)


def fingerprint_noStore_wrapper(args):
    return fingerprint_noStore(*args)


def createFingerprintsParallel(tracks, db_dir, num_jobs=1):
    db_path=db_dir+'/qfb.db'
    print(db_path)
    db = QfpDB(db_path=db_path)
    with closing(mp.Pool(processes=num_jobs)) as pool:
        fp = pool.imap(fingerprint_noStore, zip(tracks, [db_path]*len(tracks)))
        for fp_r, title in fp:
            if fp_r is not None:
                print("Storing " + title + "...")
                db.store(fp_r, title)


def find_files(data_dir):
    matches = []
    for root, dirnames, filenames in os.walk(data_dir):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            fullname = os.path.join(root, filename)
            matches.append(fullname)
    return matches


def main(data_dir, db_dir):
    reference_tracks = find_files(data_dir) #'../data/mixotic/refsongs')
    # createFingerprintsSerial(reference_tracks)
    createFingerprintsParallel(reference_tracks, db_dir, 8)


if __name__ == '__main__':
    data_dir = str(sys.argv[1])
    db_dir = str(sys.argv[2])
    main(data_dir, db_dir)
