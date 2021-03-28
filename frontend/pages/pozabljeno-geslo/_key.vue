<template>
  <b-form @submit.prevent="resetPassword">
    <p v-if="error" class="error-message text-center mt-4">
      Error
    </p>
    <p v-if="success" class="success-message text-center mt-4">
      Success
    </p>
    <div class="form-group">
      <label for="email">Vpišite novo geslo</label>
      <span v-if="errorPassword" class="error-message">Vnesite geslo.</span>
      <b-form-input
        id="password"
        v-model="password"
        :class="{ 'error-input': errorPassword }"
        type="password"
        required
        @keyup="checkPassword"
      />
    </div>
    <b-button type="submit" class="w-100 d-flex justify-content-center align-items-center position-relative text-uppercase">
      Pošlji
      <img
        src="~/assets/img/icons/arrow-right.svg"
        class="position-absolute"
        alt="right arrow"
      >
    </b-button>
    <div class="form-note text-center">
      <NuxtLink to="/prijava">
        Nazaj na prijavo
      </NuxtLink>
    </div>
  </b-form>
</template>

<script>
export default {
  layout: 'login',
  data () {
    return {
      errorPassword: false,
      error: false,
      success: false,
      password: ''
    }
  },
  methods: {
    checkPassword () {
      this.errorPassword = this.password.length === 0
    },
    async resetPassword (event) {
      const key = this.$route.params.key
      this.checkPassword()
      if (!this.errorPassword) {
        try {
          console.log('password', this.password)
          const res = await this.$axios.patch(`v1/restore-password/${key}/`, {
            new_password: this.password
          })
          console.log(res)
          this.success = true
        } catch (e) {
          this.error = true
        }
      }
    }
  }
}
</script>
