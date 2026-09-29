
# 결제 승인 서버 스펙

## 1. 기술
- Python Flask, requests.
- 결제 승인 방법은 토스페이먼츠 MCP로 "결제 승인" 문서를 검색해서 그대로 따른다.

## 2. 파일
- app.py: Flask 서버
- templates/index.html: 기존 index.html을 옮긴다.
- templates/success.html: 결제 승인 결과 표시
- templates/fail.html: 결제 실패 표시

## 3. 동작
- GET / : index.html을 표시한다.
- GET /success : paymentKey, orderId, amount를 받아 서버에서 결제 승인 API를 호출한다.
- GET /fail : code, message를 표시한다.
- successUrl은 /success, failUrl은 /fail로 변경한다.
- 결제 승인 전에 amount가 1000원인지 확인한다. 금액이 다르면 승인하지 않는다.

## 4. 보안
- 시크릿 키는 환경 변수 TOSS_SECRET_KEY에서 읽는다.
- 시크릿 키를 HTML이나 JavaScript에 넣지 않는다.
- 환경 변수가 설정되지 않았다면 서버를 시작하지 않고 오류를 표시한다.

## 5. 구현하지 않는 기능
- 데이터베이스
- 로그인
- 결제 취소
- 웹훅
  