import json
from typing import Optional
import boto3
from botocore.exceptions import ClientError

from services.csv import CSVService

class NoEntriesError(Exception):
    pass

class S3Manager():
    def __init__(self, bucket_name: str, key: str, data_model: object, **kwargs):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.key = key
        self.data_model = data_model

        if not self._key_exists():
            self._upload_empty_csv()
        

    def _key_exists(self) -> bool:
        try:
            self.s3.head_object(
                Bucket=self.bucket_name,
                Key=self.key
            )
            return True
        except ClientError:
            return False
    
    def _upload_empty_csv(self):
        body = CSVService.create_empty_csv_body(self.data_model)
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=self.key,
            Body=body
        )
        
    def _empty_csv_size(self) -> int:
        return len(CSVService.create_empty_csv_body(self.data_model))
    
    def has_entries_online(self) -> bool:
        empty_size = self._empty_csv_size()
        response = self.s3.head_object(
            Bucket=self.bucket_name,
            Key=self.key
        )
        real_size = response["ContentLength"]

        if real_size > empty_size:
            return True
        else:
            return False

    def get_max_int(self, **kwargs) -> int:
        if not self.has_entries_online():
            raise NoEntriesError("File has no entries, so cannot have a max int value either")

        # get id from first key in data model if it wasn't passed in kwargs
        column_name = kwargs.get('column_name', self.data_model._fields[0])
        return self._query_max_int(column_name)
        
    def _query_max_int(self, column_name: str) -> int:
        response = self.s3.select_object_content(
            Bucket=self.bucket_name,
            Key=self.key,
            Expression=f"select MAX(CAST(s.\"{column_name}\" as INT)) from s3object s",
            ExpressionType="SQL",
            InputSerialization={
                'CSV': {
                    'FileHeaderInfo': 'USE',
                    'QuoteEscapeCharacter': '\\',
                    'RecordDelimiter': '\n',
                    'FieldDelimiter': ',',
                    'QuoteCharacter': '"'
                }
            },
            OutputSerialization={
                'JSON': {}
            }
        )

        for event in response['Payload']:
            if 'Records' in event:
                records = event['Records']['Payload'].decode('utf-8')
                d = json.loads(records)
        
        return d.get("_1")
