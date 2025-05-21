<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let name=''
    let username = ''
    let password1 = ''
    let password2 = ''
    let email = ''
    let telecom = ''
    let phone_number = ''
    let birthdate = ''
    let gender = ''

    let errorMessage = {
    username: '',
    email: '',
    phone_number: '',
  }

  function post_user(event) {
    event.preventDefault()

    // 에러 메시지 초기화
    error = { detail: [] }
    errorMessage = { username: '', email: '', phone_number: '' }

    let url = "/api/user/create"
    let params = {
      name,
      username,
      password1,
      password2,
      email,
      telecom, 
      phone_number,
      birthdate,
      gender,
    }

    fastapi('post', url, params,
      () => {
        push('/user-login')
      },
      (json_error) => {
        error = json_error

        // ✅ 필드별 에러 메시지 분리
        const msg = json_error.detail
        if (typeof msg === 'string') {
          if (msg.includes("아이디")) errorMessage.username = msg
          else if (msg.includes("이메일")) errorMessage.email = msg
          else if (msg.includes("전화번호")) errorMessage.phone_number = msg
        }
      }
    )
  }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">회원 가입</h5>
    <Error error={error} />
    <form method="post">

        <div class="mb-3">
            <label for="username">아이디</label>
            <input type="text" class="form-control" id="username" bind:value="{username}">
        </div>

        <div class="mb-3">
            <label for="password1">비밀번호</label>
            <input type="password" class="form-control" id="password1" bind:value="{password1}">
        </div>

        <div class="mb-3">
            <label for="password2">비밀번호 확인</label>
            <input type="password" class="form-control" id="password2" bind:value="{password2}">
        </div>

        <div class="mb-3">
            <label for="email">이메일주소</label>
            <input type="text" class="form-control" id="email" bind:value="{email}">
        </div>

        <div class="mb-3">
            <label for="name">이름</label>
            <input type="text" class="form-control" id="name" bind:value="{name}">
        </div>

        <div class="mb-3">
            <label for="birthdate">생년월일</label>
            <input type="date" class="form-control" id="birthdate" bind:value={birthdate}>
        </div>

        <div class="mb-3">
            <label for="gender">성별</label>
                <select class="form-select" id="gender" bind:value={gender}>
                <option value="">선택</option>
                <option value="남">남</option>
                <option value="여">여</option>
            </select>
        </div>

        <!-- 통신사 선택 -->
        <div class="mb-3">
            <label for="telecom">통신사</label>
            <select id="telecom" class="form-select" bind:value={telecom}>
                <option value="">통신사 선택</option>
                <option value="SKT">SKT</option>
                <option value="KT">KT</option>
                <option value="LGU+">LGU+</option>
            </select>
        </div>

        <div class="mb-3">
            <label for="phone_number">전화번호</label>
            <input type="text" class="form-control" id="phone_number" bind:value={phone_number} placeholder="010-0000-0000">
            {#if errorMessage.phone_number}
                <div class="text-danger small">{errorMessage.phone_number}</div>
            {/if}
        </div>

        <button type="submit" class="btn btn-primary" on:click="{post_user}">생성하기</button>
        
    </form>
</div>