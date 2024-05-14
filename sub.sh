#!/bin/bash

# 가상 환경 생성
python3 -m venv venv

# 가상 환경 활성화
source ./venv/bin/activate 

# 의존성 설치
pip install -r requirements.txt

# FastAPI 서버 실행
uvicorn app.main:app --reload &
PID1=$!

(sleep 5; pytest -k "not test_celery" app/tests/) &
PID2=$!

# 모든 프로세스가 종료될 때까지 대기
wait $PID1 $PID2
