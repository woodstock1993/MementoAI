## 프로젝트 설명

### API (3)


**POST**
   
    - /shorten
    
        Request body
        - { "original_url": 사용자 입력 URL }

        사용자 입력 URl이 유효하지 않을 경우
        - 400 에러 발생

        사용자 입력 URL이 유효할 경우 
        - 6자리 유효한 KEY를 응답


**GET**
    
    - /{key}
        key에는 6자리 유효한 key를 넣어 요청
        
        - 유효할 경우
            301 응답 및 사용자 입력 URL로 리다이렉트

        - 유효하지 않을 경우
            404 에러 발생


    - /stats/{short_key}
        key에는 6자리 유효한 key를 넣어 요청

        - 유효할 경우
            200 응답 및 해당 유효키로 접속한 횟수 반환

        - 유효하지 않을 경우
            400 에러 발생


### Modeling

    CREATE TABLE table_name (    

        id SERIAL PRIMARY KEY,

        original_url VARCHAR,

        is_active BOOLEAN DEFAULT TRUE,

        clicks INTEGER DEFAULT 0,

        key VARCHAR UNIQUE,

        secret_key VARCHAR UNIQUE,

        expiration_date TIMESTAMP );

        # original_url: 사용자 입력 URL
        # is_active: 단축 URL이 유효한지 나타내는 상태
        # clicks: 단축 URL에 대한 접근 횟수
        # key: 단축 URL
        # secret_key: 단축 URL을 기반으로 생성되는 또하나의 key
        # expiration_date: 단축 URL 유효 시간

### 보너스

    # 만료 처리

    - /shorten api 호출 시 빠른 테스트 진행을 위해 만료 기간을 넣지 않을 경우 5초 뒤에 만료가 되는 단축 URL을 생성하였습니다.
    테스트 코드 실행 시 만료를 처리하기 위해 셀러리에 특정 task(update_urls)를 등록합니다. 해당 task가 호출 되는 시점 보다 전에 있을
    경우 is_active = False를 주어 만료처리 시킵니다.

    만료기간을 넣지 않고 싶을 경우 body에 expration_date 항목을 제거 후 요청하는 방식입니다.
    서버 시간이 한국으로 설정이 되어 있지 않을 경우 -> sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime 명령어를
    통해 적용할 수 있습니다.

    # 통계 처리

    - /stats/{short_key} 호출 시 해당하는 단축 URL이 갖는 clicks 속성을 하나 증가시키는 방향으로 API를 구현하였습니다.

    # 테스트 코드
    테스트 코드는 크게 3가지로 분류하여 tests 디렉토리 내에 작성하였습니다. 
    1. API 호출과 관련한 테스트 코드. 
    2. 해당 API 호출 시 내부에 사용되는 함수와 관련한 테스트 코드. 
    3. Celery task 관련 테스트코드 입니다.

    1번
    (test_api.py)
    
    2번
    (test_crud.py test_errors.py, test_utils.py)

    3번
    (test_celery.py)


### 데이터베이스 선택 이유

    SQLite를 선택하여 프로젝트를 진행하였습니다.SQLite는 경량이면서도 서버가 필요하지 않은 파일 기반의 데이터베이스이며, 단일 파일에 모든 데이터를 저장합니다. 
    
    설정이 간단하고 사용이 편리합니다. 특히, 소규모 프로젝트에서는 별도의 서버 설정이 용이합니다. 또한 데이터 크기가 작고 단일 사용자 환경에서 사용하기에 적합합니다. 
    
    하지만 다중 사용자 환경이거나 대량의 데이터를 다루어야 할 경우에는 성능이 제한될 수 있습니다.

### 실행 방법

    # 루트 디렉토리에 start.sh 스크립트 파일이 있습니다.
    
    # 해당 파일을 bash ./start.sh로 실행 시 아래와 같은 순서로 파일을 실행합니다.

    # 도커를 이용하여 redis 컨테이너를 로컬 환경에서 구동시키기 때문에 도커가 설치 및 실행중인 상태이어야 합니다.

    1. 가상환경 생성
    2. 가상환경 진입
    3. 의존성 생성
    4. Redis 컨테이너 실행
    5. Fast API 서버 실행
    6. Celery 실행
    7. pytest 실행