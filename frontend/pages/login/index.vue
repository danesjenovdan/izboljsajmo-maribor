<template>
  <div>
    <h1>Prijavi se!</h1>
    <Login />
    <hr class="hr-upper">
    <hr class="hr-lower">
    <b-row class="justify-content-center">
      <b-button class="mx-2">
        Log in with Facebook
      </b-button>
      <b-button class="mx-2">
        Sign in with Google
      </b-button>
    </b-row>
  </div>
</template>

<script>
import Login from '~/components/forms/Login'
export default {
  components: { Login },
  layout: 'login'
}
</script>

<style lang="scss">

</style>
