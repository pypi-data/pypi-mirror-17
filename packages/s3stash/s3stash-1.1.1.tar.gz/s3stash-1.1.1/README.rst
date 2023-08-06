=======
s3stash
=======

Very simple module that uses boto3 to stash a file in S3.

Example::

  from orgtup import AwsCredentials
  from s3stash import Stash

  bucket = 'mycoolbucket'
  credentials = AwsCredentials('myaccesskey', 'mysecretkey')
  stash = Stash(credentials, bucket)
  stash.stash_string('my cool data that I want saved to S3')


License
=======

Apache 2.0
