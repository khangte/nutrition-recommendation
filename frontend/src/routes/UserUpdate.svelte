<script>
    import { link } from 'svelte-spa-router'
    import { push } from 'svelte-spa-router'
    import fastapi from '../lib/api'
    import { username } from '../lib/store'

    let name = ''
    let email = ''
    let telecom = ''
    let phone_number = ''
    let birthdate = ''
    let gender = ''

    let message = ''

    // 정보 불러오기
    fastapi('get', '/api/user/me', {}, (json) => {
        name = json.name
        email = json.email
        phone_number = json.phone_number
        birthdate = json.birthdate
        gender = json.gender
        telecom = json.telecom
    })

    function updateUser() {
        const params = {
        name,
        email,
        phone_number,
        birthdate,
        gender,
        telecom,
        }

        fastapi('put', '/api/user/update', params,
        () => {
            message = "정보가 수정되었습니다"
            setTimeout(() => push('/user-profile'), 1500)
        },
        (err) => {
            message = `수정 실패: ${err.detail || '오류'}`
        }
        )
    }
</script>

<div class="container mt-5">
    <h4>내 정보 수정</h4>

    <div class="mb-3">
        <label for="name">이름</label>
        <input id="name" type="text" class="form-control" bind:value={name} />
    </div>

    <div class="mb-3">
        <label for="email">이메일</label>
        <input id="email" type="email" class="form-control" bind:value={email} />
    </div>

    <div class="mb-3">
        <label for="telecom">통신사</label>
        <select id="telecom" class="form-select" bind:value={telecom}>
            <option value="">선택</option>
            <option value="SKT">SKT</option>
            <option value="KT">KT</option>
            <option value="LGU+">LGU+</option>
        </select>
    </div>

    <div class="mb-3">
        <label for="phone_number">전화번호</label>
        <input id="phone_number" type="text" class="form-control" bind:value={phone_number} />
    </div>

    <div class="mb-3">
        <label for="birthdate">생년월일</label>
        <input id="birthdate" type="date" class="form-control" bind:value={birthdate} />
    </div>

    <div class="mb-3">
        <label for="gender">성별</label>
        <select id="gender" class="form-select" bind:value={gender}>
            <option value="">선택</option>
            <option value="남">남</option>
            <option value="여">여</option>
        </select>
    </div>

    <div class="d-flex justify-content-between">
        <button class="btn btn-primary" on:click={updateUser}>수정하기</button>
        <a use:link href="/user-profile" class="btn btn-secondary">취소</a>
    </div>

    {#if message}
        <div class="mt-3 alert alert-info">{message}</div>
    {/if}
</div>
