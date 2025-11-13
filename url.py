import boto3

s3 = boto3.client('s3')
url = s3.generate_presigned_url(
    'put_object',
    Params={'Bucket':'starshop-orders5', 'Key':'test.txt'},
    ExpiresIn=36000
)
print(url)
