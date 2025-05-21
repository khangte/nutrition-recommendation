<script>
    import { username } from '../lib/store'
    import { link } from 'svelte-spa-router'
    import fastapi from '../lib/api'
    import moment from 'moment'

    let name = ''
    let email = ''
    let telecom = ''
    let phone_number = ''
    let birthdate = ''
    let gender = ''
    let created_at = ''
    let last_login = ''
    let login_count = 0

    // 사용자 정보 조회
    fastapi('get', '/api/user/me', {}, 
        (json) => {
            name = json.name
            email = json.email
            birthdate = moment(json.birthdate).format('YYYY-MM-DD')
            telecom = json.telecom
            phone_number = json.phone_number
            gender = json.gender
            created_at = moment(json.created_at).format('YYYY-MM-DD HH:mm')
            last_login = json.last_login ? moment(json.last_login).format('YYYY-MM-DD HH:mm') : ''
            login_count = json.login_count
        },
        (error) => {
            console.error("사용자 정보 조회 실패", error)
        }
    )
</script>

<div class="container mt-5">
    <h3>내 정보</h3>

    <!-- 이름 -->
    <div class="row mb-2">
        <label for="name" class="col-sm-2 col-form-label">이름</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" value={name} readonly />
        </div>
    </div>

    <!-- 아이디 -->
    <div class="row mb-2">
        <label for="username" class="col-sm-2 col-form-label">아이디</label>
        <div class="col-sm-4">
            <input
            id="username"
            type="text"
            class="form-control"
            value={$username}
            readonly
            />
        </div>
    </div>

    <!-- 비밀번호 -->
    <div class="row mb-2">
        <label for="password" class="col-sm-2 col-form-label">비밀번호</label>
        <div class="col-sm-4">
            <input
            id="password"
            type="password"
            class="form-control"
            value="********"
            readonly
            />
        </div>
    </div>

    <!-- 이메일 -->
    <div class="row mb-2">
        <label for="email" class="col-sm-2 col-form-label">이메일주소</label>
        <div class="col-sm-4">
        <input
            id="email"
            type="email"
            class="form-control"
            value={email}
            readonly
        />
        </div>
    </div>

    <!-- 통신사 -->
    <div class="row mb-2">
        <label for="telecom" class="col-sm-2 col-form-label">통신사</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" value={telecom} readonly />
        </div>
    </div>

    <!-- 전화번호 -->
    <div class="row mb-2">
        <label for="phone_number" class="col-sm-2 col-form-label">전화번호</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" value={phone_number} readonly />
        </div>
    </div>

    <!-- 생년월일 -->
    <div class="row mb-2">
        <label for="birthdate" class="col-sm-2 col-form-label">생년월일</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" value={birthdate} readonly />
        </div>
    </div>

    <!-- 성별 -->
    <div class="row mb-2">
        <label for="gender" class="col-sm-2 col-form-label">성별</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" value={gender} readonly />
        </div>
    </div>

    <!-- 가입일 -->
    <div class="row mb-2">
        <label for="created_at" class="col-sm-2 col-form-label">가입일</label>
        <div class="col-sm-4">
        <input
            id="created_at"
            type="text"
            class="form-control"
            value={created_at}
            readonly
        />
        </div>
    </div>

    <!-- 마지막 로그인 -->
    <div class="row mb-2">
        <label for="last_login" class="col-sm-2 col-form-label">마지막 로그인</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" value={last_login} readonly />
        </div>
    </div>

    <!-- 로그인 횟수 -->
    <div class="row mb-2">
        <label for="login_count" class="col-sm-2 col-form-label">로그인 횟수</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" value={login_count} readonly />
        </div>
    </div>

    <hr class="my-4" />

    <div class="d-flex justify-content-between">
        <!-- 내 정보 수정 버튼: 왼쪽 -->
        <a use:link href="/user-update" class="btn btn-primary">
            내 정보 수정
        </a>

        <!-- 회원 탈퇴 버튼: 오른쪽 -->
        <a use:link href="/user-delete" class="btn btn-outline-danger">
            회원 탈퇴
        </a>
    </div>

</div>
