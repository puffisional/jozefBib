#!/usr/bin/env python
# -*- coding: utf-8 -*-
from generator import BibGenerator

generator = BibGenerator("./resources/pokus.bib")
files = generator.generate()

print(files)