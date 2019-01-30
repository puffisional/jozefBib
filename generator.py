#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import os

from pybtex.database.input import bibtex


class BibGenerator(object):
    form_template = u"./resources/form_template.tpl"
    author_template = u"./resources/author_template.tpl"

    author_default_fields = {
        u"author_index": 0,
        u"author_name": u"",
        u"author_credentials": u"x",
        u"author_percentage": 0,
        u"author_doctorand": u"nie",
        u"author_affiliation": u"Iné pracovisko - nie z UPJŠ - x",
        u"author_contact": u"",
    }

    form_default_fields = {
        u"authors": u"",
        u"title": u"",
        u"sk_title": u"",
        u"keywords": u"",
        u"sk_keywords": u"",
        u"year": u"",
        u"volume": u"",
        u"issn": u"",
        u"pages": u"",
        u"doi": u"",
        u"year": u"",
    }

    def __init__(self, database):
        self.database = database
        self.data = self._load_databsae()

    def _load_databsae(self):
        parser = bibtex.Parser()
        bib = parser.parse_file(self.database)
        bib_data = bib.lower()
        return bib_data

    def generate(self):
        entries = self.data.entries
        with open(self.form_template, "r") as fo:
            form_template = u"".join([line.decode('utf-8').strip() for line in fo.readlines()])
        with open(self.author_template, "r") as fo:
            author_template = u"".join([line.decode('utf-8').strip() for line in fo.readlines()])

        for isi_id, entry in entries.items():
            if entry.type == u"article":
                current_form_fields = copy.copy(self.form_default_fields)
                current_form_fields.update(entry.fields)

                authors = entry.persons['author']
                authors_list = []
                percentage = entry.fields["sk_podiely"].split("; ")
                if "pages" not in entry.fields:
                    print(current_form_fields["unique-id"])
                    current_form_fields["pages"] = "{}-x".format(entry.fields["volume"])
                for index, author in enumerate(authors):
                    current_autor_fileds = copy.copy(self.author_default_fields)
                    meno = " ".join(map(str, author.first_names + author.middle_names))
                    priezvisko = "".join(map(str, author.last_names))
                    current_autor_fileds["author_name"] = "{} {}".format(meno, priezvisko)
                    current_autor_fileds["author_index"] = index + 1
                    current_autor_fileds["author_percentage"] = percentage[index]
                    if priezvisko == "Bednarcik":
                        current_autor_fileds["author_affiliation"] = u"Prírodovedecká fakulta - UFV"
                    authors_list.append(author_template.format(**current_autor_fileds))

                current_form_fields["authors"] = "\n".join(authors_list)
                output_html_source = form_template.format(**current_form_fields)
                output_filename = "{}_{}.html".format(current_form_fields["year"],
                                                      current_form_fields["unique-id"].replace(":", "_"))
                with open(os.path.join("./output", output_filename), "w+") as fo:
                    fo.writelines(output_html_source.encode("utf-8"))
