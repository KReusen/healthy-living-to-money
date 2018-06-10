import io
import csv

class CSVService():
    
    @staticmethod
    def create_empty_csv_body(data_model: object) -> bytes:
        headers = data_model._fields
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        body = str.encode(output.getvalue())
        output.close()
        return body