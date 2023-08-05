# This file is part of CRFSuiteTagger.
#
# CRFSuiteTagger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CRFSuiteTagger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CRFSuiteTagger.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Aleksandar Savkov'

import gzip

from os.path import expanduser


def read_cls(cp):
    r = []
    with open(expanduser(cp), 'r') as f:
        for l in f:
            r.append(l.rstrip().split('\t'))
    return {x[0]: x[1] for x in r}


def read_emb(ep):
    if ep.endswith('.gz'):
        with gzip.open(ep, 'r') as f:
            r = []
            for l in f:
                r.append(l.split(' '))
    else:
        r = []
        with open(expanduser(ep), 'r') as f:
            for l in f:
                r.append(l.strip().split(' '))
    return {x[0]: x[1:] for x in r}


def read_brown(bp):
    r = []
    with open(expanduser(bp), 'r') as f:
        for l in f:
            r.append(l.strip().split('\t'))
    return {x[1]: x[0] for x in r}


def read_lex(lp):
    with open(lp, 'r') as fh:
        return set([l.strip() for l in fh])


def _read_afixes(ap):
    return set(open(ap, 'r').read().split('\n'))


def read_pref(pp):
    return _read_afixes(pp)


def read_suff(sp):
    return _read_afixes(sp)


def read_medsuff(sp):
    return _read_afixes(sp)


def read_medpref(sp):
    return _read_afixes(sp)


def read_verbsuff(sp):
    return _read_afixes(sp)


def read_nounsuff(sp):
    return _read_afixes(sp)


def read_adjsuff(sp):
    return _read_afixes(sp)


def read_advsuff(sp):
    return _read_afixes(sp)


def read_inflsuff(sp):
    return _read_afixes(sp)