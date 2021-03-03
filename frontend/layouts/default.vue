<template>
  <div class="wrapper">
    <div class="content">
      <Navigation />
      <Nuxt />
    </div>
    <footer>
      <Footer />
    </footer>
  </div>
</template>

<style lang="scss">

body {
  background-color: #f8f8f8;
}

.wrapper {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1 0 auto;
}

.footer {
  flex-shrink: 0;
}

</style>

<script>
import Navigation from '~/components/Navigation'
import Footer from '~/components/Footer'
export default {
  components: { Footer, Navigation }
}
</script>
