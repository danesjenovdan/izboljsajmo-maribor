<template>
  <div class="wrapper">
    <b-container fluid>
      <b-row class="logos d-flex justify-content-center justify-content-md-between align-items-center">
        <NuxtLink to="/">
          <img src="~/assets/img/izboljsajmo_maribor_logo.png" alt="Izboljšajmo Maribor LOGO" class="izboljsajmo-maribor-logo">
        </NuxtLink>
        <div class="eu-logo">
          <img src="~/assets/img/logo_med_PNG.png" alt="EU LOGO">
          <p>Projekt je sofinanciran s sredstvi Evropske unije iz Evropskega sklada za regionalni razvoj</p>
        </div>
      </b-row>
    </b-container>
    <b-container fluid class="navigation-bar">
      <Navigation />
    </b-container>
    <div class="content">
      <Nuxt />
    </div>
    <footer>
      <Footer />
    </footer>
  </div>
</template>

<script>
import Navigation from '~/components/Navigation'
import Footer from '~/components/Footer'

export default {
  components: { Footer, Navigation }
}
</script>

<style lang="scss">

html, body {
  background-color: #f8f8f8;
}

.wrapper {
  height: 100vh;
  display: flex;
  flex-direction: column;

  .logos {
    background-color: #f8f8f8;

    .eu-logo {
      width: 260px;

      img {
        width: 100%;
      }

      p {
        padding: 0 0.5rem 0.5rem 0.5rem;
        text-align: center;
        font-size: 0.75rem;
        line-height: 0.9rem;
        color: #282828;
        margin-bottom: 0.5rem;
      }

      @media (min-width: 576px) {
        width: 340px;

        p {
          padding: 0 2.6rem 0.5rem 2.6rem;
          text-align: left;
          margin-bottom: 1rem;
        }
      }
    }

    .izboljsajmo-maribor-logo {
      height: 3rem;
      margin-top: 0.5rem;

      @media (min-width: 576px) {
        height: 5rem;
        margin-left: 0.5rem;
        margin-top: 0;
      }
    }
  }

  .navigation-bar {
    position: sticky;
    top: 0;
    z-index: 1001;
  }

  .content {
    flex: 1 0 auto;
    // margin-top: 47px;
  }

  footer {
    flex-shrink: 0;
    z-index: 1;
  }
}

</style>
