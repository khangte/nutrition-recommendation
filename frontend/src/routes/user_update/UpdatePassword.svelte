<script>
    import fastapi from '../../lib/api'
    import Error from '../../components/Error.svelte'

    let currentPassword = ''
    let newPassword = ''
    let confirmPassword = ''
    let error = { detail: [] }

    function updatePassword() {
        if (newPassword !== confirmPassword) {
            error = { detail: [{ loc: ['confirmPassword'], msg: '새 비밀번호가 일치하지 않습니다.' }] }
            return
        }

        // 먼저 현재 비밀번호 검증
        fastapi('post', '/api/user/verify-password', { password: currentPassword }, 
        () => {
            // 현재 비밀번호가 맞으면 비밀번호 변경 요청
            fastapi('put', '/api/user/update-password', { password: newPassword },
            () => window.location.href = '/user-profile',
            (err) => error = err
            )
        },
        (err) => {
            // 현재 비밀번호가 틀리면 에러 출력
            error.detail.push({ loc: ['currentPassword'], msg: '비밀번호가 일치하지 않습니다.' }) 
        }
    )
    }
</script>

<div class="container mt-4">
    <h4>비밀번호 변경</h4>
    <Error {error} />

    <dif class="mb-3">
        <label for="currentPassword">현재 비밀번호</label>
        <input id="currentPassword" type="password"
        class="form-control" bind:value={currentPassword} />
    </dif>

    <div class="mb-3">
        <label for="newPassword">새 비밀번호</label>
        <input id="newPassword" type="password" class="form-control" bind:value={newPassword} />
    </div>

    <div class="mb-3">
        <label for="confirmPassword">비밀번호 확인</label>
        <input id="confirmPassword" type="password" class="form-control" bind:value={confirmPassword} />
    </div>

    <button class="btn btn-primary" on:click={updatePassword}>변경하기</button>
</div>
