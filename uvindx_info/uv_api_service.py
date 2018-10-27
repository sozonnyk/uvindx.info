import requests
from pytz import timezone
from datetime import datetime
from tzlocal import get_localzone
from .data_converter import DataConverter
import urllib3
urllib3.disable_warnings()

class UvApiService:

    def __init__(self):
        self.converter = DataConverter()

    @staticmethod
    def format_coordinate(coord):
        return '{:.2f}'.format(coord)

    @staticmethod
    def format_date(date):
        return datetime.strftime(date,'%Y-%m-%d')

    @staticmethod
    def req(url, payload={}):
        req = requests.get(url, payload, verify=False)
        req.raise_for_status()
        return req.json()

    def uv_data_string(self, lon, lat):
        today = get_localzone().localize(datetime.today())
        date = today.astimezone(timezone('Australia/Sydney'))
        params = {'longitude':UvApiService.format_coordinate(lon),
                  'latitude': UvApiService.format_coordinate(lat),
                  'date': UvApiService.format_date(date)}
        return self.converter.convert_uv_data(
                UvApiService.req('https://uvdata.arpansa.gov.au/api/uvlevel/',params))

# import code; code.interact(local=dict(globals(), **locals()))
#
