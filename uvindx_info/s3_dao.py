import boto3
import os


class S3Dao:

    s3 = boto3.resource('s3')
    bucket = os.getenv('S3_BUCKET')

    def write_file(self, name, data):
        S3Dao.s3.Object(S3Dao.bucket, name).put(Body=data, ContentType='application/json')

        # print('Writing {}'.format(name))
        # with open('./web/' + name, 'w') as outfile:
        #     outfile.write(data)


#import code; code.interact(local=dict(globals(), **locals()))
