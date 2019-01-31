# -*- coding: utf-8 -*-
import copy
import os

from pybtex.database.input import bibtex


class BibGenerator(object):
    # Form template file path
    form_template = os.path.join(u".", u"resources", u"form_template.tpl")
    # Author template file path
    author_template = os.path.join(u".", u"resources", u"author_template.tpl")

    def __init__(self, database):
        self.database = database
        self.author_default_fields = {
            u"author_index": 0,
            u"author_name": u"",
            u"author_credentials": u"x",
            u"author_percentage": 0,
            u"author_doctorand": u"nie",
            u"author_affiliation": u"Iné pracovisko - nie z UPJŠ - x",
            u"author_contact": u"",
        }
        self.form_default_fields = {
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
        }
        self.data = self._load_databsae()

    def _load_databsae(self):
        parser = bibtex.Parser()
        bib = parser.parse_file(self.database)
        data = bib.lower()
        return data

    def generate(self):
        entries = self.data.entries

        # Open form template and read as unicode
        with open(self.form_template, "r") as fo:
            form_template = u"".join([line.decode('utf-8') for line in fo.readlines()])
        # Open author template and read as unicode
        with open(self.author_template, "r") as fo:
            author_template = u"".join([line.decode('utf-8') for line in fo.readlines()])
        # List of generated files
        generated_files = []
        # Loop thru all entries
        for isi_id, entry in entries.items():
            # Process article
            if entry.type == u"article":
                # Copy default fields and extend them with article fields
                current_form_fields = copy.copy(self.form_default_fields)
                current_form_fields.update(entry.fields)
                # Get author percentage contribution
                percentage = entry.fields["sk_podiely"].split("; ")
                # Check range of pages
                if "pages" not in entry.fields:
                    current_form_fields["pages"] = u"{}-x".format(entry.fields["volume"])
                # List of article authors
                authors_list = []
                authors = entry.persons['author']
                # Loop thru all article authors
                for index, author in enumerate(authors):
                    # Copy default fields
                    current_author_fileds = copy.copy(self.author_default_fields)
                    name = u" ".join(map(str, author.first_names + author.middle_names))
                    surname = u"".join(map(str, author.last_names))
                    current_author_fileds["author_name"] = u"{} {}".format(name, surname)
                    current_author_fileds["author_index"] = index + 1
                    current_author_fileds["author_percentage"] = percentage[index]
                    if surname == u"Bednarcik":
                        current_author_fileds["author_affiliation"] = u"Prírodovedecká fakulta - UFV"
                    # Append author to the list
                    authors_list.append(author_template.format(**current_author_fileds))
                # Join all the authors into one string
                current_form_fields["authors"] = u"\n".join(authors_list)
                # Fill form template with fields
                output_html_source = form_template.format(**current_form_fields)
                # Create output filename
                output_filename = u"{}_{}.html".format(current_form_fields["year"],
                                                       current_form_fields["unique-id"].replace(u":", u"_"))
                # Create output file path
                output_file_path = os.path.join(".", "output", output_filename)
                generated_files.append(output_file_path)
                # Create output file (overwrite if exists)
                with open(output_file_path, "w+") as fo:
                    fo.writelines(output_html_source.encode("utf-8"))

        return generated_files
