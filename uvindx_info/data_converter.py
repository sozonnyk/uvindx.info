from datetime import datetime
import gviz_api

class DataConverter:

    @staticmethod
    def round_if_float(value):
        return round(value,2) if isinstance(value, float) else value

    @staticmethod
    def convert_uv_value(val):
        return {'date': datetime.strptime(val['Date'], '%Y-%m-%d %H:%M'),
            'forecast': DataConverter.round_if_float(val['Forecast']),
            'forecast_annotation':   None,
            'forecast_annotation_text':  None,
            'measured': DataConverter.round_if_float(val['Measured']),
            'measured_annotation': None,
            'measured_annotation_text': None,
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

    def convert_uv_data(self, data):

        description = {"date": ("datetime", "Time", {"role": "domain"}),
                       "forecast": ("number", "Forecast"),
                       "forecast_annotation": ('string', '', {"role": "annotation"}),
                       "forecast_annotation_text": ('string', '', {"role": "annotationText"}),
                       "measured": ("number", "Measured"),
                       "measured_annotation": ('string', '', {"role": "annotation"}),
                       "measured_annotation_text": ('string', '', {"role": "annotationText"}),
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

        for e in reversed(data):
            if e['measured'] is not None:
                e['measured_annotation'] = "%.2f @ %s" % (e['measured'], datetime.strftime(e['date'], '%H:%M'))
                break

        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)

        return data_table.ToJSon(columns_order=['date', 'low', 'low_tooltip',
                                                'medium', 'medium_tooltip',
                                                'high', 'high_tooltip',
                                                'very_high', 'very_high_tooltip',
                                                'extreme', 'extreme_tooltip',
                                                'forecast', 'forecast_annotation',
                                                "forecast_annotation_text",
                                                'measured','measured_annotation',
                                                'measured_annotation_text'])



#
# res = DataConverter().convert_uv_data(open('../tests/fixtures/uv_data.json'))
# import code; code.interact(local=dict(globals(), **locals()))
