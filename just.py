import datetime
from flask import Flask, jsonify, render_template, url_for, request, make_response, Response
import json
import craw.horoscope
import redis
from craw import qiushibaike,test,historyToday,one,yike
from apiUtil import baiduFanyi
from pointUtil import point
from functools import wraps

app = Flask(__name__)
qiushibaike=qiushibaike.craw_qiushibaike()
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun
r= redis.Redis(host='127.0.0.1', port=6379, db=0)
def has_key(keyName):

    for key in r.keys():
        if keyName==key.decode('utf-8'):
            return  True
    return False
@app.route('/qiushibaike')
@allow_cross_domain
def hello_world():
    return jsonify(qiushibaike.start())

@app.route("/point",methods=['POST','get'])
def point_info():
    p=point.Point()
    # username=request.form['username'].strip()
    # password=request.form['password'].strip()
    # data_list=p.get_detail(username,password)
    data_list = test.get_detail()
    sum_point=p.get_average_point(data_list)
    each_list=p.get_each_point(data_list)
    each_list.insert(0,{'year':'all','point':str(sum_point)})
    return json.dumps(each_list)

@app.route("/",methods=["post",'get'])
@allow_cross_domain
def detail():
    # p = point.Point()
    # data_list = p.get_detail(request.form['username'].strip(),request.form['password'].strip())
    data_list=test.get_detail()
    return jsonify(data_list)

@app.route('/horoscope/<select>',methods=['get'])
@allow_cross_domain
def horoscope(select):
    return jsonify(craw.horoscope.craw_horoscope(select))

@app.route('/fanyi/<q>',methods=['get'])
@allow_cross_domain
def fanyi(q):
    return baiduFanyi.fanyi.start(q)

@app.route('/history',methods=['post'])
@allow_cross_domain
def history():
    return jsonify(historyToday.today_history(request.form['page'],request.form['size']))

@app.route('/historyDetail',methods=['post'])
@allow_cross_domain
def historyDetail():
    return jsonify(historyToday.historyDetail(request.form['url']))

@app.route('/oneArticle',methods=['post','get'])
@allow_cross_domain
def oneArticle():
    if has_key("article_data"):
        return  jsonify(eval(r.get('article_data').decode("utf-8")))
    else:
        data=one.get_article()
        r.set('article_data', data)
        r.expire('article_data',60*60*12)
        return jsonify(data)

@app.route('/oneQuestion',methods=['post','get'])
@allow_cross_domain
def oneQuestion():
    if has_key("question_data"):
        return  jsonify(eval(r.get('question_data').decode("utf-8")))
    else:
        data=one.get_question()
        r.set('question_data', data)
        r.expire('question_data',60*60*12)
        return jsonify(data)
@app.route('/oneYikeFood',methods=['post','get'])
@allow_cross_domain
def oneYikeFood():
    f=yike.Food()
    return  Response(json.dumps(f.get_food()), mimetype='application/json')
@app.route('/oneYikePhoto',methods=['post','get'])
@allow_cross_domain
def oneYikePhoto():
    p=yike.Photo()
    return Response(json.dumps(p.get_photo()), mimetype='application/json')

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()

