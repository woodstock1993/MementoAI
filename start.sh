#!/bin/bash

# 가상 환경 생성
python3 -m venv venv

# 가상 환경 활성화
source ./venv/bin/activate 

# 의존성 설치
pip install -r requirements.txt

# Redis 컨테이너 실행
docker run -d --name test-redis -p 6379:6379 redis:alpine3.19

# FastAPI 서버 실행
uvicorn app.main:app --reload &
PID1=$!

# Celery worker 실행
(sleep 5; celery -A app.tasks.celery worker --loglevel=info) &
PID2=$!

# pytest 실행
(sleep 5; pytest) &
PID3=$!

# 모든 프로세스가 종료될 때까지 대기
wait $PID1 $PID2 $PID3
