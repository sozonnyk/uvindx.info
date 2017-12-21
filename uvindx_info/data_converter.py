from datetime import datetime
import gviz_api
import json

class DataConverter:

    @staticmethod
    def convert_uv_value(val):
        return {'date': datetime.strptime(val['Date'], '%Y-%m-%d %H:%M'),
                'forecast': val['Forecast'],
                'measured': val['Measured'],
                'low': 3,
                'low_tooltip': 'Low',
                'medium': 3,
                'medium_tooltip': 'Medium',
                'high': 2,
                'high_tooltip': 'High',
                'very_high': 3,
                'very_high_tooltip': 'Very High',
                'extreme': 4,
                'extreme_tooltip': 'Extreme'}

    @staticmethod
    def convert_city_value(val):
        return {'name': val['SiteName'].strip(),
                'lon': val['SiteLongitude'],
                'lat': val['SiteLatitude']}

    def convert_uv_data(self, data):

        description = {"date": ("datetime", "Time", {"role": "domain"}),
                       "forecast": ("number", "Forecast"),
                       "measured": ("number", "Measured"),
                       "low": ("number", "Low"),
                       "low_tooltip": ("string", "Low", {"role": "tooltip"}),
                       "medium": ("number", "Medium"),
                       "medium_tooltip": ("string", "Medium", {"role": "tooltip"}),
                       "high": ("number", "High"),
                       "high_tooltip": ("string", "High", {"role": "tooltip"}),
                       "very_high": ("number", "Very High"),
                       "very_high_tooltip": ("string", "Very High", {"role": "tooltip"}),
                       "extreme": ("number", "Extreme"),
                       "extreme_tooltip": ("string", "Extreme", {"role": "tooltip"}),
                       }

        data = list(map(DataConverter.convert_uv_value, data['GraphData']))

        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)

        return data_table.ToJSon(columns_order=['date', 'low', 'low_tooltip',
                                                'medium', 'medium_tooltip',
                                                'high', 'high_tooltip',
                                                'very_high', 'very_high_tooltip',
                                                'extreme', 'extreme_tooltip',
                                                'forecast', 'measured'])

    def convert_cities(self, data):
        cities = list(map(DataConverter.convert_city_value, data))
        cities.sort(key=lambda city: city['name'])
        return cities


#
# res = DataConverter().convert_uv_data(open('../tests/fixtures/uv_data.json'))
# import code; code.interact(local=dict(globals(), **locals()))
