<template>
  <b-container fluid>
    <b-row class="navigation justify-content-between align-items-center">
      <img src="~/assets/img/izboljsajmo_maribor_logo.png" alt="">
      <div class="">
        <NuxtLink to="/">
          Domov
        </NuxtLink>
        <NuxtLink to="/">
          O izboljšajmo Maribor
        </NuxtLink>
        <NuxtLink to="/">
          Pomoč
        </NuxtLink>
        <NuxtLink class="login" to="/login">
          Prijava
        </NuxtLink>
      </div>
    </b-row>
  </b-container>
</template>

<script>
export default {
}
</script>

<style scoped lang="scss">
.navigation {
  padding: 1rem 2rem;
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;
  background-color: #f8f8f8;

  img {
    height: 40px;
  }

  a {
    color: #606060;
    margin-left: 1rem;
    padding: 0.5rem 1rem;

    &:hover {
      text-decoration: none;
      color: #ef7782;
    }

    &.login {
      background-color: rgba(239, 119, 130, 0.3);
      border-radius: 1rem;
    }
  }
}
</style>
