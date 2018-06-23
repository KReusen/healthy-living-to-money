import io
import csv

from typing import List

from utils.models import get_field_names_from_data_model

class CSVManager():

    @staticmethod
    def create_empty_csv_body(data_model: object) -> bytes:
        headers = get_field_names_from_data_model(data_model)
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        body = str.encode(output.getvalue())
        output.close()
        return body
    
    @staticmethod
    def append_to_file(filename: str, rows: List[object], data_model: object):
        fieldnames = get_field_names_from_data_model(data_model)
        dictrows = [ row.to_dict() for row in rows ]
        with open(filename, 'a', newline='\n') as f:
            writer = csv.DictWriter(f, quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
            writer.writerows(dictrows)
