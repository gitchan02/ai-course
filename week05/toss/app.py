import os
import base64
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# 환경 변수에서 시크릿 키 가져오기
SECRET_KEY = os.environ.get('TOSS_SECRET_KEY')

if not SECRET_KEY:
    print("Error: TOSS_SECRET_KEY environment variable is not set.")
    exit(1)

# 시크릿 키 인증 헤더 생성 (SecretKey: )
# 토스페이먼츠 API 인증 방식: Base64(SecretKey + ":")
auth_header = base64.b64encode(f"{SECRET_KEY}:".encode('utf-8')).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount = request.args.get('amount')

    # 1. 금액 검증: 반드시 1000원이어야 함
    try:
        if int(amount) != 1000:
            return render_template('fail.html', code='INVALID_AMOUNT', message='요청 금액이 1000원이 아닙니다.')
    except (ValueError, TypeError):
        return render_template('fail.html', code='INVALID_AMOUNT', message='잘못된 금액 형식입니다.')

    # 2. 결제 승인 API 호출
    # API URL: https://api.tosspayments.com/v1/payments/{paymentKey}/confirm
    url = f"https://api.tosspayments.com/v1/payments/{payment_key}/confirm"
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    }
    payload = {
        "orderId": order_id,
        "amount": int(amount)
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # 결제 성공
            payment_data = response.json()
            return render_template('success.html', 
                                   payment_key=payment_data.get('paymentKey'),
                                   order_id=payment_data.get('orderId'),
                                   amount=payment_data.get('totalAmount'))
        else:
            # 결제 승인 실패
            error_data = response.json()
            return render_template('fail.html', 
                                   code=error_data.get('code', 'UNKNOWN_ERROR'),
                                   message=error_data.get('message', '결제 승인 중 오류가 발생했습니다.'))
            
    except Exception as e:
        return render_template('fail.html', code='SERVER_ERROR', message=str(e))

@app.route('/fail')
def fail():
    code = request.args.get('code')
    message = request.args.get('message')
    return render_template('fail.html', code=code, message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
