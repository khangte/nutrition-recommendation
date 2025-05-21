<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserDelete from "./routes/UserDelete.svelte"
  import UserProfile from "./routes/UserProfile.svelte"
  import UserUpdate from "./routes/UserUpdate.svelte"

  const routes = {
    '/': Home,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/user-delete': UserDelete,
    '/user-profile': UserProfile,
    '/user-update': UserUpdate,
  }
</script>

<Navigation />
<Router {routes}/>
