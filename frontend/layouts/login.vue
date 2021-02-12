<template>
  <b-container fluid class="login-container">
    <img
      src="~/assets/img/izboljsajmo_maribor_logo.png"
      class="position-absolute p-4"
      alt=""
    >
    <b-row class="vh-100 justify-content-center align-items-center">
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

  .login-window {
    background-color: #f8f8f8;
    padding: 2rem;
    border-radius: 10px;
    width: 450px;
    max-height: 80%;
    overflow-y: scroll;

    h1 {
      font-weight: 700;
      text-align: center;
      //margin-bottom: 1.5rem;
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
