import json
import os
import datetime
from database import DataBaseExecution

def get_daily_obs():
    db = DataBaseExecution()
    date = datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists(date + '.json'):
        try:
            check_query = "SELECT COUNT(*) as count FROM obsData WHERE date = %s"
            db.cursor.execute(check_query, (date))
            result = db.cursor.fetchone()
            
            if result['count'] > 0:
                select_query = "SELECT * FROM obsData WHERE date = %s"
                db.cursor.execute(select_query, (date))
                res = db.cursor.fetchall()
                with open(date + '.json', 'w') as file:
                    json.dump(res[0], file)
            else:
                res = "当日数据未上传"
                raise ValueError(res)
        except Exception as e:
            return e
        finally:
            db.close()