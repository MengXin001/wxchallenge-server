import logging
from flask import Flask, request, jsonify
from datetime import datetime

from meteva import Meteva

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger(__name__)

@app.route('/api/getObsData', methods=['GET'])
def get_obs_data():
    date = request.args.get('date')
    db = DataBaseExecution()
    try:
        check_query = "SELECT COUNT(*) as count FROM obsData WHERE date = %s"
        db.cursor.execute(check_query, (date))
        result = db.cursor.fetchone()
        
        if result['count'] > 0:
            select_query = "SELECT * FROM obsData WHERE date = %s"
            db.cursor.execute(select_query, (date))
            res = db.cursor.fetchall()
            return jsonify({"msg": "200", "data": res[0]}), 200
        else:
            res = "数据不存在"
            return jsonify({"msg": "400", "error": res}), 400
    except Exception as e:
        return jsonify({"msg": "500", "error": e}), 500
    finally:
        db.close()

@app.route('/api/postObsData', methods=['POST'])
def post_obs_data():
    data = request.get_json()
    
    data_format = {
        "user_name": "string",
        "max_temp": "float",
        "min_temp": "float", 
        "wind_speed": "float",
        "precipitation": "float"
    }
    for key in data_format.keys():
        if key not in data:
            return jsonify({"msg": "400", "error": f"缺失参数：'{key}'"}), 400

    now = datetime.now().strftime('%Y-%m-%d')
    
    db = DataBaseExecution()
    try:
        query = """
            INSERT INTO obsData (date, max_temp, min_temp, wind_speed, precipitation)
            VALUES (%s, %s, %s, %s, %s)
        """
        db.cursor.execute(query, (
            now,
            data['max_temp'], 
            data['min_temp'], 
            data['wind_speed'], 
            data['precipitation']
        ))
        db.submit()
        return jsonify({"msg": "数据提交成功"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"msg": "500", "error": f"{str(e)}"}), 500
    finally:
        db.close()

@app.route('/api/meteva', methods=['POST'])
def wxchallenge():
    data_format = {
        "user_name": "string",
        "max_temp": "float",
        "min_temp": "float", 
        "wind_speed": "float",
        "precipitation": "float"
    }
    now = datetime.now()
    if now.hour >= 20:
        return jsonify({"msg": "200", "data": "当日提交已经截止"}), 200

    data = request.get_json()
    mock_ac = {
        "max_temp": 32.0,
        "min_temp": 28.0,
        "wind_speed": 8.0,
        "precipitation": 0.2
    }
    try:
        for key in data_format.keys():
            if key not in data:
                return jsonify({"msg": "400", "error": f"缺失参数：'{key}'"}), 400
        meteva_instance = Meteva(data, mock_ac)
        res = meteva_instance.res()
        return jsonify({"msg": "200", "data": res}), 200
    except Exception as e:
        logger.error(f"error: {e}")
        return jsonify({"msg": "400", "error": f"{e}"}), 500

if __name__ == '__main__':
    app.run(port=11451, threaded=True)
