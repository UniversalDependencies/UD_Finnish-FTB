* Origin

The UD version of FinnTreeBank 1 was derived from FinnTreeBank 1 2014
by a scripted mapping of labels and some restructuring in an attempt
to conform approximately to the UD Finnish model.

Unannotated linguistic material in FinnTreeBank 1 2014 was adapted
from the examples in Ison suomen kieliopin verkkoversio (The Web
Version of the Large Grammar of Finnish, VISK), available on-line as
<http://scripta.kotus.fi/visk>, and annotations originally produced
and further revised in FIN-CLARIN projects in the Department of Modern
Languages, University of Helsinki.


* Differences from the UD Finnish model

Some differences from the UD Finnish model remain unaddressed.

Surface words that have an adverb or a conjunction fused with a
following negative verb are separated into two tokens in the
FinnTreeBank model. The UD version keeps them as such but adds the
unannotated joined token before the two.

A small number of multiword sequences remain as single tokens.

Most punctuation tokens are linked to a nearby token instead of a
clause head.

The xcomp relation is not used in the mapping (the distinction between
xcomp and comp is not supported in the underlying FinnTreeBank model).

As a catchall, the dep relation is used as intended when a more proper
mapping could not be determined.

Some FinnTreeBank annotations are retained in the MISC field.


* Splitting

The treebank was split into training, development, and test sets by
repeatedly taking 8 sentences into training set, 1 into development
set, and 1 into test set.


* Statistics

Tree count:  19097
Word count:  161984
Token count: 161682
Dep. relations: 26 of which 2 language specific
POS tags: 14
Category=value feature pairs: 64


* Sources

VISK = Auli Hakulinen, Maria Vilkuna, Riitta Korhonen, Vesa Koivisto,
Tarja Riitta Heinonen and Irja Alho 2004: Iso suomen
kielioppi. Helsinki: Suomalaisen Kirjallisuuden Seura. Online version.
Available: http://scripta.kotus.fi/visk URN:ISBN:978-952-5446-35-7

<http://www.ling.helsinki.fi/kieliteknologia/tutkimus/treebank/>

fin-clarin@helsinki.fi

* Changelog

** UD v1.1 -> UD v1.2

Negative=Yes was changed to Negative=Neg
The data was re-split to resolve train/dev/test overlaps within the treebank as well as with UD_Finnish

** UD v1.2 -> UD v1.3

A major revision of the underlying FinnTreebank 1 with some manually
annotated UD analyses (e.g. xcomp; these annotations are visible in
the UD version as Alt in the MISC field).

Adjusted the conversion script to better match the universal
guidelines (e.g. finite verbs now have VerbForm, again using PART) and
the Finnish guidelines (e.g. now using nsubj:cop, csubj:cop,
nmod:own).

Duplicates in the underlying FinnTreebank 1 have been removed and
sentences are now labeled with unique identifiers like "ekvje-124"
(the part before the hyphen identifies the sentence within
FinnTreebank 1).

--- Machine-readable metadata ---
Documentation status: stub
Data source: semi-automatic
Data available since: UD v1.1
License: CC BY 4.0
Genre: grammar-examples
Contributors: Piitulainen, Jussi; Nurmi, Hanna
