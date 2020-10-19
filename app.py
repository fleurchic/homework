from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    who_received = request.form['who_give']
    phonenumber_received = request.form['phonenumber_give']
    what_received = request.form['what_give']
    whereto_received = request.form['whereto_give']
    email_received = request.form['email_give']

    # DB에 삽입할 order 만들기
    order = {
        'name': who_received,
        'phone_number': phonenumber_received,
        'order': what_received,
        'address': whereto_received,
        'email': email_received
    }
    # orders에 order 저장하기
    db.orders.insert_one(order)

    return jsonify({'result': 'success', 'msg': '주문에 성공했습니다.'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    # 1. DB에서 order 정보 모두 가져오기
    orders = list(db.orders.find({}, {'_id': 0}))
    # 2. 성공 여부 & 주문 목록 반환하기
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)