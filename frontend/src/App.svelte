<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserDelete from "./routes/UserDelete.svelte"
  import UserProfile from "./routes/UserProfile.svelte"
  import UserUpdate from './routes/user_update/UpdateUser.svelte'
  import VerifyPassword from './routes/auth/VerifyPassword.svelte'
  import UpdatePassword from './routes/user_update/UpdatePassword.svelte'
    import UpdateUser from './routes/user_update/UpdateUser.svelte';

  const routes = {
    '/': Home,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/user-delete': UserDelete,
    '/user-profile': UserProfile,
    '/user-update': UserUpdate,
    '/update-password': UpdatePassword,
    // '/verify-password/password':{
    //   component: VerifyPassword,
    //   props: { next: '/update-password' } // 명시적으로 전달
    // },
    
  }
</script>

<Navigation />
<Router {routes}/>
