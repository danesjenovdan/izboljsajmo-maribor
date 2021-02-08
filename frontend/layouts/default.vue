<template>
  <div>
    <Navigation />
    <Nuxt />
    <Footer />
  </div>
</template>

<style lang="scss">

</style>
<script>
import Navigation from '~/components/Navigation'
import Footer from '~/components/Footer'
export default {
  components: { Footer, Navigation }
}
</script>
