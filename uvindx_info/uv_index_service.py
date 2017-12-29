from .uv_api_service import UvApiService
from .s3_dao import S3Dao
import json
import os


class UvIndexService:

    def main(self):
        api = UvApiService()
        s3 = S3Dao()
        cities = json.load(open(os.path.dirname(os.path.abspath(__file__))+'/cities.json'))

        for city in cities:
            try:
                data = api.uv_data_string(city['lon'], city['lat'])
                s3.write_file('data/{}.json'.format(city['name']), data)
            except Exception as e:
                print("Exception: {0}".format(e))
                pass


