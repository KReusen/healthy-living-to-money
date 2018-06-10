import boto3
from botocore.exceptions import ClientError

from services.csv import CSVService
from models.run import Run

class S3RunsManager():
    def __init__(self, bucket_name: str, key: str = 'runs.csv'):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.bucket = boto3.resource('s3').Bucket(bucket_name)
        self.key = key

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
        body = CSVService.create_empty_csv_body(Run)
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=self.key,
            Body=body
        )
        
    def _empty_csv_size(self) -> int:
        return len(CSVService.create_empty_csv_body(Run))
    
    def file_has_entries(self) -> bool:
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

    def get_latest_run_id(self):
        pass
    