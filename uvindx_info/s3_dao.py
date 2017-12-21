import boto
import os


class S3Dao:

    def write_file(self, name, data):
        print(os.getenv('S3_BUCKET'))
        print('Writing {}'.format(name))

        with open(name, 'w') as outfile:
            outfile.write(data)


#import code; code.interact(local=dict(globals(), **locals()))
