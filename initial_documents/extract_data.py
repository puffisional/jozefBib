from pybtex.database.input import bibtex
from pybtex.database import BibliographyData, Entry
import numpy as np


parser = bibtex.Parser()

# importing bibtex database
bib = parser.parse_file('pokus.bib')
bib_data = bib.lower()

# getting ids of bitbex cards
ids = bib_data.entries.keys()

# tu si ulozime jeden zaznam z databazy s konkretnym id do premennej a
a = bib_data.entries['isi:000429838900068']

# tu je ulozeny typ zaznamu (article, inproceeding, book, ...)
a.type

# toto je vlastne samotny zaznam (typovo je to slovnik, dictionary) 
# ktory pozostava z dvojic atribut : hodnota
a.fields

# toto je list atributov
a.fields.keys()

# toto je list hodnot
a.fields.values()

# tu je priklad ako pristupit k nejakej hodnote atributu
print "Nazov clanku v AJ je :\n {:s}\n".format(a.fields['title'])
print "Nazov clanku v SJ je :\n {:s}\n".format(a.fields['sk_title'])

# k zoznamu autorov sa pristpuje trochu inac, mena su uz naparsovane do instancii typu Person
# vies potom robit rozne veci s formatovanim mien

print 'Tu je vypisany zoznam autorov clanku:'
authors = a.persons['author']
nr = len(authors)
for i in range(nr):
	meno = " ".join(map(str, authors[i].first_names + authors[i].middle_names))
	priezvisko = "".join(map(str, authors[i].last_names))
	print "{:02d}. {:s} {:s}".format(i+1, meno, priezvisko)


