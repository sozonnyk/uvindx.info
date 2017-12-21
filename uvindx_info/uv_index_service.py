from .uv_api_service import UvApiService
from .s3_dao import S3Dao
import json


class UvIndexService:

    def main(self):
        api = UvApiService()
        s3 = S3Dao()

        cities = api.cities()
        s3.write_file('./web/data/cities.json', json.dumps(cities))

        for city in cities:
            data = api.uv_data_string(city['lon'], city['lat'])
            s3.write_file('./web/data/{}.json'.format(city['name']), data)


def lambda_handler(event, context):
    UvIndexService().main()
