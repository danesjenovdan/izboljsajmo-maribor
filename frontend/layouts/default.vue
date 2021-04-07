<template>
  <div class="wrapper">
    <div class="navigation">
      <Navigation />
    </div>
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

  .navigation {
    nav {
      position: fixed;
      z-index: 500;
    }
  }

  .content {
    flex: 1 0 auto;
    margin-top: 66px;
  }

  footer {
    flex-shrink: 0;
    z-index: 1;
  }
}

</style>
