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
    <b-row class="justify-content-center align-items-md-center">
      <div class="login-window">
        <Nuxt />
      </div>
    </b-row>
  </b-container>
</template>

<style lang="scss">

.login-container {
  background-image: url('~assets/img/login-background-image.png');
  background-size: cover;
  background-position: center;

  &>.row {
    @media (min-width: 768px) {
      height: 100vh;
    }
  }

  .logo {
    text-align: center;

    @media (min-width: 768px) {
      position: absolute;
    }
  }

  .login-window {
    background-color: #f8f8f8;
    padding: 2rem;
    overflow-y: scroll;

    @media (min-width: 768px) {
      max-height: 80%;
      border-radius: 10px;
    }

    h1 {
      font-weight: 700;
      text-align: center;
    }

    a {
      font-size: 0.75rem;
      font-style: italic;
      font-weight: 300;
      color: black;
      text-decoration: underline;

      &:hover {
        color: #ef7782;
      }
    }

    hr {
      width: calc(450px + 4rem);
      margin-left: -2rem;
    }
  }
}

</style>
