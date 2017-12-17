from datetime import datetime


class DataConverter:

    @staticmethod
    def convert_uv_value(val):
        return {'date': datetime.strptime(val['Date'], '%Y-%m-%d %H:%M'),
                'forecast': val['Forecast'],
                'measured': val['Measured']}

    @staticmethod
    def convert_city_value(val):
        return {'name': val['SiteName'].strip(),
                'lon': val['SiteLongitude'],
                'lat': val['SiteLatitude']}

    def convert_uv_data(self, data):
        return list(map(DataConverter.convert_uv_value, data['GraphData']))

    def convert_cities(self, data):
        return list(map(DataConverter.convert_city_value, data))
#
# res = DataConverter().convert_uv_data(open('../tests/fixtures/uv_data.json'))
# import code; code.interact(local=dict(globals(), **locals()))
