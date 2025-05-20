<script>
  import { is_login, username } from "../lib/store"
</script>

<div class="container mt-5 text-center">
  <h2 class="mb-4">🏠 홈 화면</h2>

  {#if $is_login}
    <p>👋 {$username}님 환영합니다!</p>
    <p>상단 메뉴에서 로그아웃하거나 다른 기능을 이용해보세요.</p>
  {:else}
    <p>로그인 후 더 많은 기능을 이용할 수 있습니다.</p>
    <p>상단 메뉴에서 로그인 또는 회원가입을 진행해보세요.</p>
  {/if}
</div>
