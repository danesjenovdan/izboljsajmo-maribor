<template>
  <div class="text-center">
    <h1>Potrdite e-naslov</h1>
    <p v-if="error" class="message d-flex justify-content-center align-items-center position-relative">
      <IconDanger />Prišlo je do napake.
      <span class="position-absolute" @click="error = false">Zapri</span>
    </p>
    <p v-if="success" class="message d-flex justify-content-center align-items-center position-relative">
      <IconSuccess />Račun je uspešno ustvarjen.
      <span class="position-absolute" @click="success = false">Zapri</span>
    </p>
    <NuxtLink to="/prijava">
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
      console.log(this.$route.params.key)
      try {
        const res = await this.$axios.get(`v1/confirm-email/${this.$route.params.key}`)
        console.log(res)
        this.success = true
      } catch (e) {
        this.error = true
      }
    }
  }
}
</script>
