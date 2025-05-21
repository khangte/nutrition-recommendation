# FastAPI 회원가입 구현

> ## 실행코드
> - FastAPI 실행 코드
> ```bash
> uvicorn main:app --host 0.0.0.0 --port 8000
> ```
> - Svelte 실행코드
> ```bash
> npm run dev
> ```

---

> ## 개발환경 구성 
> ### 시스템 환경
> - 가상화 플랫폼: VirtualBox + Ubuntu 22.04 Server
> - 메모리: 8GB
> - 프로세서: 4개 이상(pycharm, vscode 사용 때문)
> - 비디오메모리: 16MB
> - 모니터개수: 1개
> - 저장소 메모리: 16~25GB
> - 네트워크: NAT + 포트포워딩
> ### 백엔드
> - 프레임워크: FastAPI
> - 서버 실행: Uvicorn
> - 개발 환경: PyCharm
> ### 프론트엔드
> - 프레임워크: Svelte
> - UI 라이브러리: Bootstrap 5.3.6
> - 개발환경: Visual Studio Code
> ### 데이터베이스 
> - RDBMS: MySQL 
> - 구동 방식: Docker Container
> - 데이터 유지: Docker Volume
> ### 배포용 GitHub Repository
> - [GitHub/khangte](https://github.com/khangte/fastapi-login-test)

---

## 파일 구조
```
login-test/
├── domain/
│   └── user/
│       ├── user_crud.py
│       ├── user_router.py
│       └── user_schema.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Error.svelte
│   │   │   └── Navigation.svelte
│   │   ├── lib/
│   │   │   ├── api.js
│   │   │   └── store.js
│   │   ├── routes/
│   │   │   ├── auth
│   │   │   │   └── VerifyPassword.svelte
│   │   │   ├── user_update
│   │   │   │   ├── UpdatePassword.svelte
│   │   │   │   └── UpdateUser.svelte
│   │   │   ├── Home.svelte
│   │   │   ├── UserCreate.svelte
│   │   │   ├── UserDelete.svelte
│   │   │   ├── UserLogin.svelte
│   │   │   └── UserProfile.svelte
│   │   ├── app.css
│   │   ├── App.svelte
│   │   ├── main.js
│   │   └── vite-env.d.ts
│   ├── .env
│   ├── .gitignore
│   ├── index.html
│   ├── jsconfig.json
│   ├── package-lock.json
│   └── package.json
├── migrations/
│   ├── versions/
│   └── env.py
├── .env
├── alembic.ini
├── database.py
├── main.py
├── models.py
├── README.md
└── requirements.txt
```

---

> ## uv 가상환경
> - 가상환경 생성
> ```
> $ uv venv
> ```
> - 가상환경 활성화
> ```bash
> $ source .venv/bin/activate 
> ```

> ## Svelte 설치
> ```bash
> $ npm create vite@latest frontend -- --template svelte
> $ cd frontend
> $ npm install
> ```
> - jsconfig.json 타입스크립트 사용 안함 => false로 변경
> ```json
> 파일명: /frontend/jsconfig.json
> {
>   (...생락...)
>   "checkJs": false
>   (...생락...)
> }
> ```

---

> ## MySQL 서버 구성
> - Docker + Volume
> - Windows Docker Desktop 환경
> 
> ✅ **1. Docker Volume 생성** (Windows PowerShell에서 실행 가능)
> ```bash
> docker volume create mysql-volume
> ```
>
> ---
>
> ✅ **2. MySQL 컨테이너 실행** (Windows Docker Desktop 기준)
>
> ```bash
> docker run -d ^
>   --name my-mysql ^
>   -e MYSQL_ROOT_PASSWORD=1234 ^
>   -e MYSQL_DATABASE=testdb ^
>   -p 3306:3306 ^
>   -v mysql-volume:/var/lib/mysql ^
>   --restart unless-stopped ^
>   mysql:8.0
> ```
>
> 🔸 `--restart unless-stopped`: Windows 재시작 후 Docker Desktop이 다시 실행되면 컨테이너도 자동 실행됨  
> 🔸 `-v mysql-volume:/var/lib/mysql`: MySQL 데이터를 Docker Volume에 저장하여 컨테이너를 재생성해도 데이터 보존  
> 🔸 `MYSQL_DATABASE=testdb`: 초기 데이터베이스 자동 생성
>
> ---
>
> ✅ **3. MySQL 컨테이너 상태 확인**
>
> ```bash
> docker ps
> ```
>
> ---
> 
> ✅ **4. PowerShell에서 현재 IP 확인 (ifconfig는 Linux 명령어입니다)**
>
> ```powershell
> ipconfig
> ```
>
> 🔍 `이더넷 어댑터`, `Wi-Fi`, 또는 `vEthernet (Default Switch)` 중  
> **IPv4 주소** 항목에서 `192.168.x.x` 또는 `10.x.x.x` 와 같은 IP를 찾습니다.
> ```
> 예시: 
> 이더넷 어댑터 이더넷 2:
>    IPv4 주소 . . . . . . . . . : 192.0.0.0
> ```
>
> ---
>
> ✅ **5. Ubuntu (WSL or VirtualBox)에서 MySQL 접속**
>
> ```bash
> 예시: 
> mysql -h 192.168.0.101 -P 3306 -u root -p
> ```
> 비밀번호: 1234
> 
> 📌 Ubuntu에서 `localhost → Docker(MySQL)`에 접근하려면 Docker가 `3306` 포트를 로컬에 노출하고 있어야 합니다.  
> 위 `-p 3306:3306` 설정으로 자동 처리됩니다.
>
> ---
> 
> ✅ **6. FastAPI의 `SQLALCHEMY_DATABASE_URL` 설정**
>
> ```python
> 예시:
> SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@192.168.0.101:3306/testdb"
> ```
> 📌 `localhost`로 접속이 되지 않을 경우 반드시 위처럼 **Windows의 실제 IP 주소를 지정**해야 합니다.
>

---

> Alembic 마이그레이션 과정
> 1. Alembic 초기화
> ```bash
> alembic init migrations
> ```
> 2. 설정 파일 수정
> - ```alembic.ini```수정
> - ```migrations/env.py```수정
> ```python
>  from models
>  target_metadata = models.Base.metadata
> ```
> 3. 변경사항 감지하고 마이그레이션 파일 생성
> ```bash
> alembic revision --autogenerate
> ```
> 4. DB에 적용
> ```bash
> alembic upgrade head
> ```

---

> ## 기능 구현 절차
> 1. 스키마 생성
> 2. CRUD 함수 작성
> 3. 라우터 생성
> 4. Svelte 컴포넌트 등록
> 5. 컴포넌트 파일 작성

---

