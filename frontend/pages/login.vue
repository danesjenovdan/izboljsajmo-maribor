<template>
  <div>
    <h1>Prijavi se!</h1>
    <Login />
    <hr class="hr-upper">
    <hr class="hr-lower">
    <b-row class="justify-content-center">
      <button class="facebook-button my-2 my-md-0 mx-2">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><path fill="#039be5" d="M24 5A19 19 0 1 0 24 43A19 19 0 1 0 24 5Z" /><path fill="#fff" d="M26.572,29.036h4.917l0.772-4.995h-5.69v-2.73c0-2.075,0.678-3.915,2.619-3.915h3.119v-4.359c-0.548-0.074-1.707-0.236-3.897-0.236c-4.573,0-7.254,2.415-7.254,7.917v3.323h-4.701v4.995h4.701v13.729C22.089,42.905,23.032,43,24,43c0.875,0,1.729-0.08,2.572-0.194V29.036z" /></svg>
        Log in with Facebook
      </button>
      <button class="google-button my-2 my-md-0 mx-2">
        <img src="~/assets/img/icons/google-logo.png" alt="google icon">
        Sign in with Google
      </button>
    </b-row>
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

img, svg {
  height: 1.5rem;
  width: 1.5rem;
  margin-right: 0.5rem;
}

button {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  border: lightgray solid 1px;

  &:hover {
    background-color: #5a6268;
    color: white;
  }
}

.facebook-button {
  background-color: #1877f2;
  color: white;
}

</style>
