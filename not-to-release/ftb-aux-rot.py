'''Undo FinnTreeBank native auxiliary verb convention in UD version by
rotating the local trees at such verbs. The auxiliary is raised to be
the (local) main verb, the old main verb lowered to be its child, old
child nodes (of the old main verb) that precede the old auxiliary
raised to the new main verb in order to not introduce non-planar
structure (maybe they even belong there properly, who knows).

One hopes to make the UD validator happy, or at least a bit happier.
Two bits, even?

NB! stdin to stdout only.

'''

from itertools import chain, groupby
from re import match
from sys import stdin, stderr

def istoken(line):
    '''For groupby, but watch out as technically token-range lines are
    among these, and they do belong in a sentence, but they must be
    taken out temporarily to have a densely indexed token sequence.

    '''
    return line[:1].isdigit()

# CoNLL-U has 10 fields, approximately so named (could not resist
# making ID and HD the same length in characters for *this rot*)
ID, WORD, BASE, UPOS, XPOS, FEAT, HD, REL, _, MISC = range(10)

def rot(sentence):
    '''Rotate AUX and VERB so they become VERB and VERB; at this point,
    sentence consists of token records at positive indices, ID and HD
    numeric, ID the same as the index, so any token-range likes must
    be kept somewhere else.

    '''

    # (should get rid of that k)
    for k, token in enumerate(sentence):
        # skip placeholder at index 0
        if k == 0: continue

        # finally, is there any surgery to do here?
        # careful: modifying the tree in-place!
        if ( token[UPOS] == 'AUX' and
             token[REL] in (
                 # exclude 'root' in particular: nothing to rotate
                 'aux', ) and
             token[BASE] in {
                 # skip words that the validator rejects
                 'alkaa',
                 'auttaa',
                 'ehtiä',
                 'ennättää',
                 'haluta',
                 'huolia',
                 'joutaa',
                 'jättää',
                 'jäädä',
                 'kannattaa',
                 'kelvata',
                 'keretä',
                 'keritä',
                 'kuulua',
                 'kärsiä',
                 'käydä',
                 'lakata',
                 'meinata',
                 'näkyä',
                 'näyttää',
                 'osata',
                 'osoittautua',
                 'ottaa',
                 'parata',
                 'pakata',
                 'passata',
                 'pyrkiä',
                 'pystyä',
                 'ruveta',
                 'ryhtyä',
                 'saada',
                 'sattua',
                 'sopia',
                 'tahtoa',
                 'tavata',
                 'toimittaa',
                 'tulla',
                 'tuntua',
                 'uhata',
                 'vaikuttaa',
                 'viitsiä',
                 'yrittää'} ):
            NEW = token
            OLD = sentence[token[HD]]

            # some AUX are sibling to copula, child to something other
            # than a VERB, and should not be rotated like those that
            # are child to a VERB
            if OLD[UPOS] == 'VERB':
                for sub in (
                        # children of OLD on the other side of NEW, raise
                        # them to NEW so that the arcs will still not
                        # cross; use whatever relation they had to OLD
                        tok for tok in sentence[1:]
                        if tok[HD] == OLD[ID]
                        if ( tok[ID] < NEW[ID] < OLD[ID] or
                             OLD[ID] < NEW[ID] < tok[ID] )):
                    sub[HD] = OLD[ID] # aka k
                else:
                    # THEN raise NEW to the position that OLD had, and
                    # also make it VERB instead of (presumably) AUX
                    NEW[UPOS], NEW[HD], NEW[REL] = 'VERB', OLD[HD], OLD[REL]

                    # finally lower OLD to be a child of NEW but what
                    # should the relation be now? instead of aux? TODO
                    # find out what sort of relations TNPP produces and
                    # replace 'wev' with some such, possibly depending on
                    # the actual word, NEW[WORD] or NEW[BS], that used to
                    # be an aux but was just re-analyzed as a main verb
                    #
                    # relation 'ccomp' out of thin air
                    OLD[HD], OLD[REL] = NEW[ID], 'ccomp'
            else:
                pass

            # so be done with this token - but can OLD have been an
            # aux? because then NEW would still be an aux, which was
            # precisely the problem being solved? also hoping that any
            # other aux of OLD between NEW and OLD will be properly
            # handled already (though for a very heuristic value of
            # "properly") and in particular will not hijack any of
            # those former childer of OLD that were already raised to
            # NEW

for issentence, group in groupby(stdin, istoken):
    if not issentence:
        print(*group, sep = '', end = '')
        continue

    # reify to filter twice: for token lines to represent the
    # sentence, and for token-range lines to keep the annotation
    _lines = list(group)
    
    # sentence is stored as records (and let MISC have the line
    # terminator, AND insert a bogus placeholder at index 0)
    sentence = [
        line.split('\t')
        for line in chain(['(no such token)\n'],
                          (line for line in _lines
                           if match('\d+\t', line)))
    ]

    # interpret ID and HD in sentence as numbers
    for k, token in enumerate(sentence):
        if k == 0: continue
        token[ID] = int(token[ID])
        token[HD] = int(token[HD])

    # sanity check
    for k, token in enumerate(sentence):
        assert k == 0 or token[ID] == k

    # store token-range annotations separately, to be shipped at the
    # corresponding token in the end
    annotations = {
        int(mo.group(1)) : line
        for line in _lines
        for mo in [match('(\d+)-\d+\t', line)]
        if mo
    }

    rot(sentence)
    for k, token in enumerate(sentence):
        if k == 0: continue
        print(annotations.get(token[ID], ''), end = '')
        print(*token, sep = '\t', end = '')

# some heuristically usable observations follow

'''

(most frequent AUX in TNPP-parsed STT_1992_result.vrt)

    220 tarvita	AUX
   1239 täytyä	AUX
   2310 ette	AUX
   5738 saattaa	AUX
   6400 aikoa	AUX
   6654 pitää	AUX
   6726 joutua	AUX
  31094 voida	AUX
  87945 ei	AUX
 438432 olla	AUX

(most frequent AUX/relation in TNPP-parsed STT_1992_result.vrt)

   5709 saattaa	AUX	aux
   6168 aikoa	AUX	aux
   6569 joutua	AUX	aux
   6575 pitää	AUX	aux
  14887 olla	AUX	cop:own
  30883 voida	AUX	aux
  51207 olla	AUX	aux:pass
  87314 ei	AUX	aux
 129639 olla	AUX	aux
 239857 olla	AUX	cop

(most frequent relation in TNPP-parsed STT_1992_result.vrt)

   2000 ette	aux
   5727 saattaa	aux
   6314 aikoa	aux
   6748 pitää	aux
   6929 _	aux
   7143 joutua	aux
  30900 voida	aux
  51220 olla	aux:pass
  87862 ei	aux
 129684 olla	aux

'''
