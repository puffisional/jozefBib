# -*- coding: utf-8 -*-
import argparse
import os

from generator import BibGenerator

parser = argparse.ArgumentParser()
# Specify any database file using --database argument
parser.add_argument("--database", default=os.path.join(".", "resources", "pokus.bib"))
args = parser.parse_args()

# Initialize bib file generator
generator = BibGenerator(args.database)
# Generate files
files = generator.generate()

print(files)
