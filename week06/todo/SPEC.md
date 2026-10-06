# 1. 개요
사용자가 할 일을 등록하고, 완료 상태를 관리하며, 필요 없는 항목을 삭제할 수 있는 심플한 웹 기반 Todo 애플리케이션입니다.

# 2. 기술
- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: Pure HTML & CSS (External Frameworks excluded)

# 3. 파일 구성
- `app.py`: Flask 애플리케이션 로직, 라우팅 및 데이터베이스 연동
- `database.db`: 할 일 데이터가 저장되는 SQLite 데이터베이스 파일
- `static/css/style.css`: 웹앱의 레이아웃 및 디자인을 담당하는 순수 CSS 파일
- `templates/index.html`: 사용자 인터페이스를 제공하는 HTML 템플릿

# 4. 동작 규칙

| 라우트 (Route) | 메서드 | 입력 | 결과 (Response) |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | 없음 | 전체 할 일 목록이 포함된 메인 페이지 출력 |
| `/add` | `POST` | `title` (text) | 제목 공백 제거 후 저장 (빈 제목 제외), 메인 페이지로 리다이렉트 |
| `/toggle/<id>` | `POST` | `id` (int) | 해당 ID의 `is_completed` 상태를 반전, 메인 페이지로 리다이렉트 |
| `/delete/<id>` | `POST` | `id` (int) | 해당 ID의 항목 삭제, 메인 페이지로 리다이렉트 |

**[데이터 처리 세부 규칙]**
- **공백 처리**: 입력받은 제목의 앞뒤 공백은 자동으로 제거(trim)한다.
- **빈 제목**: 공백을 제거한 후 내용이 없는 경우, 아무것도 저장하지 않고 즉시 메인 페이지(`/`)로 리다이렉트한다.
- **긴 제목**: 제목이 100자를 초과할 경우, DB에는 전체를 저장하되 UI상에서는 CSS(`text-overflow: ellipsis`)를 통해 생략 처리하여 레이아웃을 유지한다.
- **예외 ID 처리**: 요청된 `id`가 DB에 존재하지 않을 경우, 서버 에러(500)를 발생시키지 않고 단순히 메인 페이지(`/`)로 안전하게 리다이렉트한다.

# 5. 화면
- **메인 화면**: 
    - 상단: 새로운 할 일을 입력할 수 있는 텍스트 입력창과 '추가' 버튼
    - 중앙: 할 일 목록 영역 (제목, 생성 시각, 완료 체크 버튼, 삭제 버튼이 포함된 리스트 형태)
    - 디자인: 외부 프레임워크 없이 깔끔하고 가독성 높은 타이포그래피와 간결한 여백 활용

# 6. 테스트
Flask의 `test_client`를 사용하여 다음 항목들을 검증합니다.

| 번호 | 요청 (Request) | 기대하는 결과 (Expected Result) |
| :--- | :--- | :--- |
| 1 | `GET /` | `200 OK` 및 초기 빈 목록 화면 출력 |
| 2 | `POST /add` (title="  Work  ") | `302 Redirect` 및 DB에 "Work"로 저장되었는지 확인 |
| 3 | `POST /add` (title="   ") | `302 Redirect` 및 DB에 새로운 행이 추가되지 않았는지 확인 |
| 4 | `POST /add` (title="Very Long Title..." x 10) | `302 Redirect` 및 긴 문자열이 정상 저장되었는지 확인 |
| 5 | `POST /toggle/<existing_id>` | `302 Redirect` 및 해당 항목의 `is_completed` 값이 반전되었는지 확인 |
| 6 | `POST /toggle/<non_existent_id>` | `302 Redirect` 및 에러 없이 메인 페이지로 복귀하는지 확인 |
| 7 | `POST /delete/<existing_id>` | `302 Redirect` 및 해당 항목이 DB에서 완전히 삭제되었는지 확인 |
| 8 | `POST /delete/<non_existent_id>` | `302 Redirect` 및 에러 없이 메인 페이지로 복귀하는지 확인 |
| 9 | `GET /` (데이터 존재 시) | `200 OK` 및 저장된 할 일 항목들이 HTML 내에 포함되어 있는지 확인 |
| 10 | `POST /add` (title="A") -> `POST /toggle/<id>` | 연속 요청 시 완료 상태가 정확히 반영되는지 확인 |

# 7. 실행 방법
1. Python 환경 설치 (Flask 포함)
2. `pip install flask` 실행
3. `python app.py` 명령어로 서버 실행
4. 브라우저에서 `http://127.0.0.1:5000` 접속

# 8. 하지 않는 것
- 사용자 로그인 및 계정 관리 기능 구현 안 함
- 할 일의 제목 수정(Edit) 기능 구현 안 함
- Bootstrap 등 외부 CSS 프레임워크 사용 안 함
- JavaScript 프레임워크(React, Vue 등) 및 순수 JS 라이브러리 사용 안 함