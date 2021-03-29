<template>
  <b-form @submit.prevent="resetPassword">
    <p v-if="error" class="error-message text-center mt-4">
      Uporabnik s tem e-naslovom ne obstaja.
    </p>
    <p v-if="success" class="success-message text-center mt-4">
      Preverite svoj e-poštni predal, kamor smo vam poslali navodila za obnovo gesla.
    </p>
    <div class="form-group">
      <label for="email">Vpišite svoj e-naslov</label>
      <span v-if="errorEmail" class="error-message">Vnesite veljaven e-naslov.</span>
      <p class="form-note">
        Na e-naslov boste prejeli spletno povezavo za ponastavitev gesla za prijavo.
      </p>
      <b-form-input
        id="email"
        v-model.trim="email"
        :class="{ 'error-input': errorEmail }"
        type="email"
        required
        @keyup="checkEmail"
      />
    </div>
    <b-button type="submit" class="w-100 d-flex justify-content-center align-items-center position-relative text-uppercase">
      Pošlji
      <ArrowRightIcon class="position-absolute" />
    </b-button>
    <div class="form-note text-center">
      <NuxtLink to="/prijava">
        Nazaj na prijavo
      </NuxtLink>
    </div>
  </b-form>
</template>

<script>
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'

export default {
  components: { ArrowRightIcon },
  data () {
    return {
      errorEmail: false,
      error: false,
      success: false,
      email: ''
    }
  },
  methods: {
    checkEmail () {
      this.error = false
      this.errorEmail = this.email.length === 0
    },
    async resetPassword (event) {
      this.checkEmail()
      if (!this.errorEmail) {
        try {
          await this.$store.dispatch('resetPassword', { email: this.email })
          this.success = true
        } catch (e) {
          this.error = true
        }
      }
    }
  }
}
</script>

<style lang="scss">

</style>
