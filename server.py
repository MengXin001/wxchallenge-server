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

@app.route('/api/meteva', methods=['GET'])
def wxchallenge():
    date = request.args.get('date')
    db = DataBaseExecution()
    try:        
        select_query = "SELECT * FROM wp_WxChallengeSU_test"
        db.cursor.execute(select_query)
        res = db.cursor.fetchall()
        accu_ep_latest_list = {}
        for item in res:
            accu_ep_latest_list[item["user_nickname"]] = item["accu_ep_latest"]
        check_query = "SELECT COUNT(*) as  count FROM wp_WxChallengeObs WHERE obs_date = %s"
        db.cursor.execute(check_query, (date))
        result = db.cursor.fetchone()
        if result['count'] > 0:
            select_query = "SELECT * FROM wp_WxChallengeObs WHERE obs_date = %s"
            db.cursor.execute(select_query, date)
            res = db.cursor.fetchall()
            obsdata = {
                "max_temp": res[0]["max_temp_obs"],
                "min_temp": res[0]["min_temp_obs"],
                "wind_speed": res[0]["max_wind_speed_obs"],
                "precipitation": res[0]["precipitation_obs"]
            }
        else:
            obsdata = "数据不存在"
        select_query = "SELECT * FROM wp_WxChallengeCont_test WHERE forecast_date = %s"
        db.cursor.execute(select_query, (date))
        res = db.cursor.fetchall()
        
        for user in res:
            data = {
                "max_temp": user["max_temp"],
                "min_temp": user["min_temp"],
                "wind_speed": user["max_wind_speed"],
                "precipitation": user["precipitation"]
            }
            meteva_instance = Meteva(data, obsdata)
            res = meteva_instance.res()
            score = res["total_error"]
            t_score = accu_ep_latest_list[user["user_nickname"]]
            t_score = float(0 if t_score is None else t_score)
            t_score += res["total_error"]
            update_sql = "UPDATE wp_WxChallengeCont_test SET score = %s, t_score = %s WHERE user_nickname = %s AND forecast_date = %s"
            params = (score, t_score, user["user_nickname"], date)
            db.cursor.execute(update_sql, params)
            db.submit()
            update_sql = "UPDATE wp_WxChallengeSU_test SET accu_ep_latest = %s WHERE user_nickname = %s"
            params = (t_score, user["user_nickname"])
            db.cursor.execute(update_sql, params)
            db.submit()
        db.close()
        
        return jsonify({"msg": "200"}), 200
    except Exception as e:
        logger.error(f"error: {e}")
        return jsonify({"msg": "400"}), 400


if __name__ == '__main__':
    app.run(port=11451, threaded=True)
