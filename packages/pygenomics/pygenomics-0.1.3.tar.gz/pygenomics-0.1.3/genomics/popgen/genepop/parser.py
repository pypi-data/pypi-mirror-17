# -*- coding: utf-8 -*-
'''
.. module:: genomics.popgen.genepop
   :synopsis:
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>
'''


def _get_indiv(line):
    indiv_name, marker_line = line.split(',')
    markers = marker_line.replace('\t', ' ').split(' ')
    markers = [marker for marker in markers if marker != '']
    if len(markers[0]) in [2, 4]:  # 2 digits per allele
        marker_len = 2
    else:
        marker_len = 3
    try:
        allele_list = [(int(marker[0:marker_len]),
                       int(marker[marker_len:]))
                       for marker in markers]
    except ValueError:  # Haploid
        allele_list = [(int(marker[0:marker_len]),)
                       for marker in markers]
    return indiv_name, allele_list, marker_len


def read(handle):
    """Parses a handle containing a Genepop file.

       handle is a file-like object that contains a GenePop record.
    """
    record = Record(handle)
    record.comment_line = str(handle.readline()).rstrip()
    # We can now have one loci per line or all loci in a single line
    # separated by either space or comma+space...
    # We will remove all commas on loci... that should not be a problem
    sample_loci_line = str(handle.readline()).rstrip().replace(',', '')
    all_loci = sample_loci_line.split(' ')
    record.loci_list.extend(all_loci)
    line = handle.readline()
    while line != '':
        line = line.rstrip()
        if line.upper() == 'POP':
            record.stack.append('POP')
            break
        record.loci_list.append(line)
        line = handle.readline()
    next_line = handle.readline().rstrip()
    indiv_name, allele_list, record.marker_len = _get_indiv(next_line)
    record.stack.append(next_line)
    return record


class Record(object):
    '''Holds information from a GenePop record.

    Members:
    marker_len         The marker length (2 or 3 digit code per allele).

    comment_line       Comment line.

    loci_list          List of loci names.


    The generator will only work once. If you want to read a handle
    twice you have to re-open it!

    The object will be a generator for the data.

    data can either be:
        () - an empty tuple - marking a new population or
        An individual which is something like
            ('Ind1', [(1, 1), (3, None), (200, 201)],
            In the case above the individual is called Ind1,
            has three diploid loci. For the second loci, one of the alleles
            is unknown.

    '''
    def __init__(self, handle):
        self.handle = handle
        self.marker_len = 0
        self.comment_line = ""
        self.loci_list = []
        self.populations = []
        self.stack = []

    def __iter__(self):
        return self

    def __next__(self):
        for handle in [self.stack, self.handle]:
            for line in handle:
                line = line.rstrip()
                if line.upper() == 'POP':
                    yield ()
                else:
                    indiv_name, allele_list, marker_len = _get_indiv(line)
                    clean_list = []
                    for locus in allele_list:
                        mk_real = []
                        for al in locus:
                            if al == 0:
                                mk_real.append(None)
                            else:
                                mk_real.append(al)
                        clean_list.append(tuple(mk_real))
                    yield indiv_name, clean_list
        raise StopIteration()
