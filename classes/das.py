"""this file will get the request and generate img in base 64.

and parse to the vision the vision will parse the file
and then return the obj that google returns
ehen thid file will apply the regex and return to the user import re import.
"""

import re
import base64
from pdf2image import convert_from_bytes
from classes.vision import vision
import tempfile
import io
import json
#
cnpj = re.compile('[0-9]{2}[.]{1}[0-9]{3}[.]{1}[0-9]{3}[/]{1}[0-9]{4}[-]{1}[0-9]{2}')
curr = re.compile('^\s*(?:[1-9]\d{0,2}(?:\.\d{3})*|0)(?:,\d{1,2}){1}$')
comp_date = re.compile('(0[1-9]|10|11|12)\/20[0-9]{2}$')
due_date = re.compile('^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$')
doc_number = re.compile('^([0-9]{2}.)([0-9]{2}.)([0-9]{5}.)([0-9]{7}-)([0-9]{1})$')
barcode_sec = re.compile('^([0-9]{12}|[0-9]{11})*$')
barcode_string = re.compile('^[0-9]*$')
barcode = re.compile('^(([0-9]{11})(\ ){1}([0-9]{1})(\ ){1}){3}([0-9]{11})(\ ){1}([0-9]{1})$')
cpf = re.compile('[0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2}')

class Das():
    """."""
#
    def __init__(self, temp_file):
        """."""
        self._temp_file = temp_file
#
    def format(self, raw):
        """."""
        cnpjs = []
        currs = []
        comp_dates = []
        due_dates = []
        barcodes = []
        cpfs = []

        for index, text in enumerate(raw):
            if cnpj.match(text.description):
                cnpjs.append(text.description)
            if cpf.match(text.description):
                cpfs.append(text.description)
            if curr.match(text.description):
                currs.append(text.description)
            if comp_date.match(text.description):
                comp_dates.append(text.description)
            if due_date.match(text.description):
                due_dates.append(text.description)
            if barcode_sec.match(text.description):
                i = index
                code = ''
                while i <= len(raw) - 1 and (barcode_sec.match(raw[i].description) or barcode_string.match(raw[i].description)):
                    code += raw[i].description
                    i += 1
                if len(code) == 48 and barcode_string.match(code):
                    barcodes.append(code)

        return {"cnpj": set(cnpjs).pop() if len(cnpjs) != 0 else None, "cpf": set(cpfs).pop() if len(cpfs) != 0 else None, "curr": max([float(c.replace('.', '', 1).replace(',', '.')) for c in currs]) if len(currs) != 0 else None, "comp_date": set(comp_dates).pop() if len(comp_dates) != 0 else None, "due_date": set(due_dates).pop() if len(due_dates) != 0 else None, "barcode": set(barcodes).pop() if len(barcodes) != 0 else None}
    def get_temp_file(self):
        """."""
        return self._temp_file

    def parse(self):
        """."""
        with open(self._temp_file, 'rb') as f:
            binary = f.read()
            if self._temp_file.split('.').pop().lower() == 'pdf':
                temp_file = tempfile.NamedTemporaryFile(prefix='{}_'.format(self._temp_file))
                image = convert_from_bytes(binary)[0]
                with io.BytesIO() as out:
                    image.save(out, format='JPEG')
                    temp_file.write(out.getvalue())
                return self.format(vision(temp_file))
        return json.dumps(self.format(vision(f=binary)))

