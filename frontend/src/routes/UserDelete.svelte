<script>
  import { access_token, username, is_login } from "../lib/store"
  import { push } from 'svelte-spa-router'

  let password = ''
  let result = ''

  if (!$is_login) {
    push('/user-login')
  }

  async function deleteUser() {
    if (!password.trim()) {
      result = "비밀번호를 입력해주세요."
      return
    }

    // 1단계: 비밀번호 확인 요청
    const verifyRes = await fetch("http://localhost:8000/api/user/verify-password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + $access_token
      },
      body: JSON.stringify({ password })
    })

    if (!verifyRes.ok) {
      result = "비밀번호가 일치하지 않습니다."
      return
    }

    const ok = confirm("정말 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다.")
    if (!ok) return

    // 2단계: 실제 탈퇴 요청
    const res = await fetch("http://localhost:8000/api/user/delete", {
      method: "DELETE",
      headers: {
        "Authorization": "Bearer " + $access_token
      }
    })

    if (res.ok) {
      alert("회원 탈퇴가 완료되었습니다.")
      $access_token = ''
      $username = ''
      $is_login = false
      push('/user-login')
    } else {
      const err = await res.json()
      result = `탈퇴 실패: ${err.detail || "오류 발생"}`
    }
  }
</script>

<div class="container my-5" style="max-width: 500px">
  <h2 class="mb-4">회원 탈퇴</h2>
  <p>회원 탈퇴를 진행하려면 비밀번호를 다시 입력해주세요.</p>

  <div class="mb-3">
    <input type="password" class="form-control" placeholder="비밀번호" bind:value={password} />
  </div>

  {#if result}
    <div class="alert alert-warning">{result}</div>
  {/if}

  <button class="btn btn-danger" on:click={deleteUser}>회원탈퇴</button>
  <button class="btn btn-secondary ms-2" on:click={() => push('/')}>홈으로</button>
</div>
