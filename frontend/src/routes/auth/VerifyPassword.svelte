<script>
    export let next

    import fastapi from '../../lib/api'
    import Error from '../../components/Error.svelte'
    import { push } from 'svelte-spa-router'

    let password = ''
    let error = { detail: [] }

    function verify() {
        fastapi('post', '/api/user/verify-password', { password },
        () => {
            if (next) push(next)
            else alert('리디렉션 경로가 지정되지 않았습니다.')
        },
        (err) => error = err
        )
    }
</script>

<div class="container mt-4">
    <h4>비밀번호 확인</h4>
    <Error {error} />

    <div class="mb-3">
        <label for="password">현재 비밀번호</label>
        <input id="password" type="password" class="form-control" bind:value={password} />
    </div>

    <button class="btn btn-primary" on:click={verify}>확인</button>
</div>
