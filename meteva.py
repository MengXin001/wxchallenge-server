import json
import numpy as np

def check_type(data):
    return isinstance(data, (int, float))

class Meteva:
    def __init__(self, forecast, actual):
        self.forecast = forecast
        self.actual = actual
        self.errors = {
            "temperature_error": 0,
            "wind_speed_error": 0,
            "precip_error": 0
        }
        
        self.wind_coef = 0.5
        self.precip_coef = [0.08, 0.06, 0.04, 0.02]
        for i in ["max_temp","min_temp","wind_speed","precipitation"]:
            if check_type(self.forecast[i]) == False:
                raise ValueError(f"参数数据类型不合法: {i}")
        self.calc_total_error()
        
    def calc_temperature_error(self):
        max_temp_diff = np.abs(self.forecast["max_temp"] - self.actual["max_temp"])
        min_temp_diff = np.abs(self.forecast["min_temp"] - self.actual["min_temp"])
        
        self.errors["temperature_error"] = max_temp_diff + min_temp_diff

    def calc_wind_speed_error(self):
        wind_speed_diff = np.abs(self.forecast["wind_speed"] - self.actual["wind_speed"])

        self.errors["wind_speed_error"] = self.wind_coef * wind_speed_diff
    
    def calc_precip_error(self):
        min_standard = min(self.actual["precipitation"], self.forecast["precipitation"])
        max_standard = max(self.actual["precipitation"], self.forecast["precipitation"])
        
        if min_standard < 2.5:
            diff = min(2.5, max_standard) - min_standard
            self.errors["precip_error"] += self.precip_coef[0] * diff / 0.1

        if max_standard > 2.5 and min_standard < 6.5:
            diff = min(6.5, max_standard) - max(2.5, min_standard)
            self.errors["precip_error"] += self.precip_coef[1] * diff / 0.1

        if max_standard > 6.5 and min_standard < 12.5:
            diff = min(12.5, max_standard) - max(6.5, min_standard)
            self.errors["precip_error"] += self.precip_coef[2] * diff / 0.1

        if max_standard > 12.5:
            diff = max_standard - max(12.5, min_standard)
            self.errors["precip_error"] += self.precip_coef[3] * diff / 0.1

    def calc_total_error(self):
        self.calc_temperature_error()
        self.calc_wind_speed_error()
        self.calc_precip_error()
        self.total_error = self.errors["temperature_error"] + self.errors["wind_speed_error"] + self.errors["precip_error"]

    def res(self):
        return {
            "errors": self.errors,
            "total_error": self.total_error
        }

if __name__ == '__main__':
    f = {
        "max_temp": 33.0,
        "min_temp": 29.0,
        "wind_speed": 10.0,
        "precipitation": 21.0
    }
    
    a = {
        "max_temp": 32.0,
        "min_temp": 27.0,
        "wind_speed": 8.0,
        "precipitation": 11
    }
    
meteva_instance = Meteva(f, a)
print(meteva_instance.res())