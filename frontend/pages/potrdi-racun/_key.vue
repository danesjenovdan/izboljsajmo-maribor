<template>
  <div class="text-center">
    <h1>
      Zaključek registracije
    </h1>
    <p v-if="error" class="message error d-flex justify-content-center align-items-center position-relative">
      <IconDanger />Prišlo je do napake. Za pomoč nam pišite na <a href="mailto:im@maribor.si">im@maribor.si</a>.
      <span class="position-absolute" @click="error = false">Zapri</span>
    </p>
    <p v-if="success" class="message success d-flex justify-content-center align-items-center position-relative">
      <IconSuccess />Čestitke! Račun je uspešno ustvarjen.
      <span class="position-absolute" @click="success = false">Zapri</span>
    </p>
    <NuxtLink class="back-button" to="/prijava">
      Nazaj na prijavo
    </NuxtLink>
  </div>
</template>

<script>
import IconDanger from '~/assets/img/icons/danger.svg?inline'
import IconSuccess from '~/assets/img/icons/success.svg?inline'

export default {
  components: { IconDanger, IconSuccess },
  layout: 'login',
  data () {
    return {
      success: false,
      error: false
    }
  },
  mounted () {
    this.confirmEmail()
  },
  methods: {
    async confirmEmail () {
      try {
        await this.$axios.get(`v1/confirm-email/${this.$route.params.key}`)
        this.success = true
      } catch (e) {
        this.error = true
      }
    }
  }
}
</script>

<style>
.message a {
  color: black;
  font-weight: 500;
  padding-left: 4px;
}
</style>
