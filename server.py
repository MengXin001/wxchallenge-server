import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from meteva import Meteva

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger(__name__)

@app.route('/api/getUserInfo', methods=['GET'])
def get_user_info():
    db = DataBaseExecution()
    try:
        check_query = "SELECT COUNT(*) as count FROM wp_WxChallengeSU"
        db.cursor.execute(check_query)
        result = db.cursor.fetchone()
        
        if result['count'] > 0:
            select_query = "SELECT user_nickname, user_school FROM wp_WxChallengeSU"
            db.cursor.execute(select_query)
            res = db.cursor.fetchall()
            return jsonify({"msg": "200", "data": res}), 200
        else:
            res = "数据不存在"
            return jsonify({"msg": "400", "error": res}), 400
    except Exception as e:
        return jsonify({"msg": "500", "error": e}), 500
    finally:
        db.close()

@app.route('/api/getRank', methods=['GET'])
def get_user_rank():
    date = request.args.get('date')
    usertype = request.args.get('usertype')
    db = DataBaseExecution()
    try:
        check_query = "SELECT COUNT(*) as count FROM wp_WxChallengeCont WHERE forecast_date = %s"
        db.cursor.execute(check_query, (date))
        result = db.cursor.fetchone()
        
        if result['count'] > 0:
            if usertype=="beginner":
                select_query = "SELECT * FROM wp_WxChallengeCont WHERE forecast_date = %s AND is_beginner = 1"
            elif usertype=="u_beginner":
                select_query = "SELECT * FROM wp_WxChallengeCont WHERE forecast_date = %s AND is_beginner = 0"
            else:
                select_query = "SELECT * FROM wp_WxChallengeCont WHERE forecast_date = %s"
            db.cursor.execute(select_query, (date))
            res = db.cursor.fetchall()
            
            return jsonify({"msg": "200", "data": res}), 200
        else:
            res = "数据不存在"
            return jsonify({"msg": "400", "error": res}), 400
    except Exception as e:
        return jsonify({"msg": "500", "error": e}), 500
    finally:
        db.close()

@app.route('/api/getUserScore', methods=['GET'])
def get_user_score():
    user = request.args.get('user')
    date = request.args.get('date')
    db = DataBaseExecution()
    try:
        check_query = "SELECT COUNT(*) as count FROM wp_WxChallengeCont WHERE user_nickname = %s"
        db.cursor.execute(check_query, (user))
        result = db.cursor.fetchone()
        
        if result['count'] > 0:
            select_query = "SELECT * FROM wp_WxChallengeCont WHERE user_nickname = %s AND forecast_date = %s"
            db.cursor.execute(select_query, (user, date))
            res = db.cursor.fetchall()
            return jsonify({"msg": "200", "data": res}), 200
        else:
            res = "数据不存在"
            return jsonify({"msg": "400", "error": res}), 400
    except Exception as e:
        return jsonify({"msg": "500", "error": e}), 500
    finally:
        db.close()

@app.route('/api/getObsData', methods=['GET'])
def get_obs_data():
    date = request.args.get('date')
    db = DataBaseExecution()
    try:
        check_query = "SELECT COUNT(*) as count FROM wp_WxChallengeObs WHERE obs_date = %s"
        db.cursor.execute(check_query, (date))
        result = db.cursor.fetchone()
        
        if result['count'] > 0:
            select_query = "SELECT * FROM wp_WxChallengeObs WHERE obs_date = %s"
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
        "precipitation": 16
    }
    try:
        for key in data_format.keys():
            if key not in data:
                return jsonify({"msg": "400", "error": f"缺失参数: '{key}'"}), 400
        meteva_instance = Meteva(data, mock_ac)
        res = meteva_instance.res()
        
        return jsonify({"msg": "200", "data": res}), 200
    except Exception as e:
        logger.error(f"error: {e}")
        return jsonify({"msg": "400", "error": e}), 400

if __name__ == '__main__':
    app.run(port=11451, threaded=True)
