<template>
  <div>
    <h1>Prijavi se!</h1>
    <Login />
  </div>
</template>

<script>
import Login from '~/components/forms/Login'

export default {
  components: { Login },
  layout: 'login',
  middleware: 'auth'
}
</script>

<style scoped lang="scss">

</style>
