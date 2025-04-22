import json
import math
import numpy as np
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError

class CustomJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        try:
            data = json.loads(stream.read().decode('utf-8'))
            return self._clean_nan_values(data)
        except json.JSONDecodeError as exc:
            raise ParseError('JSON parse error - %s' % str(exc))

    def _clean_nan_values(self, data):
        if isinstance(data, dict):
            return {k: self._clean_nan_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._clean_nan_values(item) for item in data]
        elif isinstance(data, float) and (math.isnan(data) or np.isnan(data)):
            return None
        return data 