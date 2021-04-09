<template>
  <b-form @submit.prevent="resetPassword">
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
      <ArrowRightIcon class="position-absolute" />
    </b-button>
    <p v-if="error" class="message d-flex justify-content-center align-items-center position-relative">
      <IconDanger />Prišlo je do napake.
      <span class="position-absolute" @click="error = false">Zapri</span>
    </p>
    <p v-if="success" class="message d-flex justify-content-center align-items-center position-relative">
      <IconSuccess />Vaše geslo je nastavljeno.
      <span class="position-absolute" @click="success = false">Zapri</span>
    </p>
    <div class="form-note text-center">
      <NuxtLink to="/prijava">
        Nazaj na prijavo
      </NuxtLink>
    </div>
  </b-form>
</template>

<script>
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'
import IconDanger from '~/assets/img/icons/danger.svg?inline'
import IconSuccess from '~/assets/img/icons/success.svg?inline'

export default {
  components: { ArrowRightIcon, IconDanger, IconSuccess },
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
