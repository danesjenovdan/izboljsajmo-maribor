<template>
  <div>
    <h1>Potrdite e-naslov</h1>
    <div v-if="success" class="text-center">
      <p>Račun je uspešno ustvarjen.</p>
      <NuxtLink to="/prijava">
        Prijavite se
      </NuxtLink>
    </div>
    <div v-if="error" class="text-center">
      <p>Prišlo je do napake.</p>
    </div>
  </div>
</template>

<script>
export default {
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
