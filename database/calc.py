from datetime import datetime
from utils import DataBaseExecution

class DataCalc:
    def __init__(self, date):
        self.date = date
        self.db = DataBaseExecution()
        self.data = None
        self.get_data()

    def get_data(self):
        try:
            check_query = "SELECT COUNT(*) as count FROM wp_WxChallengeCont WHERE forecast_date = %s"
            self.db.cursor.execute(check_query, (self.date))
            result = self.db.cursor.fetchone()
            if result['count'] > 0:
                select_query = "SELECT min_temp, max_temp, max_wind_speed, precipitation FROM wp_WxChallengeCont WHERE forecast_date = %s"
                self.db.cursor.execute(select_query, (self.date))
                res = self.db.cursor.fetchall()
                self.data = res
                self.calc_data(self.data)
            else:
                raise ValueError("数据不存在")
        except Exception as e:
            raise ValueError(e)
        finally:
            self.db.close()

    def calc_data(self, data):
        max_wind_speed = 0
        max_temp = 0
        min_temp = 0
        precipitation = 0
        try:
            user_num = len(data)
            for item in data:
                max_wind_speed += item['max_wind_speed']
                max_temp += item['max_temp']
                min_temp += item['max_wind_speed']
                precipitation += item['precipitation']
            self.avg_max_wind_speed = round(max_wind_speed / user_num, 1)
            self.avg_max_temp = round(max_temp / user_num, 1)
            self.avg_min_temp = round(min_temp/ user_num, 1)
            self.avg_precipitation = round(precipitation / user_num, 1)
            
            self.avg_obj = {
                "max_temperature_error": self.avg_max_temp,
                "min_temperature_error": self.avg_min_temp,
                "wind_speed_error": self.avg_max_wind_speed,
                "precip_error": self.avg_precipitation
            }
        except Exception as e:
            raise ValueError(e)

if __name__ == '__main__':
    calc = DataCalc("2024-08-25")
    print(calc.avg_obj)