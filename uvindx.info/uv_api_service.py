import requests
from datetime import datetime

class UvApiService:

    @staticmethod
    def format_coordinate(coord):
        return '{:.2f}'.format(coord)

    @staticmethod
    def format_date(date):
        return datetime.strftime(date,'%Y-%m-%d')

    @staticmethod
    def req(url, payload={}):
        req = requests.get(url, payload)
        req.raise_for_status()
        return req.json()

    def cities(self):
        return UvApiService.req('https://uvdata.arpansa.gov.au/api/categoriesSites')

    def uv_data(self,lon,lat,date):
        params = {'longitude':UvApiService.format_coordinate(lon),
                  'latitude': UvApiService.format_coordinate(lat),
                  'date': UvApiService.format_date(date)}
        return UvApiService.req('https://uvdata.arpansa.gov.au/api/uvlevel/',params)

# import code; code.interact(local=dict(globals(), **locals()))
#
