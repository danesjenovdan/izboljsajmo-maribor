<template>
  <b-container fluid class="login-container">
    <div class="logo">
      <NuxtLink to="/predlogi">
        <img
          src="~/assets/img/izboljsajmo_maribor_logo.png"
          class="p-4"
          alt="Izboljšajmo Maribor logo"
        >
      </NuxtLink>
    </div>
    <b-row class="justify-content-center align-items-sm-center">
      <b-col cols="12" md="9" lg="6" xl="4">
        <div class="login-window">
          <Nuxt />
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<style lang="scss">

.login-container {
  background-image: url('~assets/img/login-background-image.png');
  background-size: cover;
  background-position: center;

  &>.row {
    height: 100vh;
  }

  .logo {
    text-align: center;

    @media (min-width: 576px) {
      position: absolute;
    }
  }

  .login-window {
    background-color: #f8f8f8;
    padding: 2rem;
    border-radius: 10px;

    h1 {
      font-weight: 700;
      text-align: center;
    }

    a {
      font-size: 0.75rem;
      font-style: italic;
      font-weight: 500;
      color: black;
      text-decoration: underline;

      &:hover {
        color: #ef7782;
      }
    }

    hr {
      margin-left: -2rem;
      margin-right: -2rem;
    }
  }
}

</style>
