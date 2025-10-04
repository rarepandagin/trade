import boto3

class Boto3Class:
    def __init__(self, bucket_name):
        self.aws_access_key_id = "AKIA2FRY6ZG6WAN35FRI"
        self.aws_secret_access_key = "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"
        self.bucket_name = bucket_name

        self.get_client_from_new_session()

        self.bucket_location = self.s3.get_bucket_location(Bucket=self.bucket_name)

    def get_client_from_new_session(self):
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

        self.s3 = session.client("s3")







    def upload_file_to_s3(self, file_path, file_name):
        self.get_client_from_new_session()

        self.s3.upload_file(file_path, self.bucket_name, file_name)

        object_url = f"https://{self.bucket_name}.s3.{self.bucket_location['LocationConstraint']}.amazonaws.com/{file_name}"

        return object_url


    def delete_file_from_s3(self, file_name):
        self.get_client_from_new_session()

        self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)


    def delete_files_from_s3(self, file_names):
        self.get_client_from_new_session()

        objects_to_delete = [{'Key': file_name} for file_name in file_names]

        if len(objects_to_delete) > 0:
            self.s3.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objects_to_delete})


    def list_files(self, prefix):
        self.get_client_from_new_session()

        return self.s3.list_objects(Bucket=self.bucket_name, Prefix=prefix)



    def delete_files_by_prefix(self, prefix):
        self.get_client_from_new_session()

        objects_to_delete = self.s3.list_objects(Bucket=self.bucket_name, Prefix=prefix)

        delete_keys = {'Objects' : []}
        delete_keys['Objects'] = [{'Key': k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]

        if len(delete_keys['Objects']) > 0:
            self.s3.delete_objects(Bucket=self.bucket_name, Delete=delete_keys)

