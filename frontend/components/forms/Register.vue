<template>
  <form @submit.prevent="register">
    <p v-if="errorRegister" class="error-message text-center mt-4">
      Registracija ni uspela.
    </p>
    <div class="form-group">
      <label for="username">Ime in priimek (uporabniško ime)</label>
      <span v-if="errorUsername" class="error-message">Vpišite uporabniško ime.</span>
      <p class="form-note">
        Ime, ki ga prikazujemo ob vaših objavah.
      </p>
      <b-form-input
        id="username"
        v-model="form.username"
        :class="{ 'error-input': errorUsername }"
        name="username"
        type="text"
        required
        @keyup="checkUsername"
      />
    </div>
    <div class="form-group">
      <label for="email">E-naslov</label>
      <span v-if="errorEmail" class="error-message">Vpišite e-naslov.</span>
      <b-form-input
        id="email"
        v-model.trim="form.email"
        :class="{ 'error-input': errorEmail }"
        type="email"
        required
        @keyup="checkEmail"
      />
    </div>
    <div class="form-group">
      <label for="phone">Telefonska številka</label>
      <span v-if="errorPhone" class="error-message">Vpišite telefonsko številko.</span>
      <b-form-input
        id="phone"
        v-model="form.phone"
        :class="{ 'error-input': errorPhone }"
        type="tel"
        required
        @keyup="checkPhone"
      />
    </div>
    <div class="form-group">
      <label for="password">Geslo</label>
      <span v-if="errorPassword" class="error-message">Vpišite geslo.</span>
      <b-form-input
        id="password"
        v-model="form.password"
        :class="{ 'error-input': errorPassword }"
        type="password"
        required
        @keyup="checkPassword"
      />
    </div>
    <b-button type="submit" class="w-100 d-flex justify-content-center align-items-center position-relative">
      ZAKLJUČI REGISTRACIJO
      <img
        src="~/assets/img/icons/arrow-right.svg"
        class="position-absolute"
        alt="arrow icon"
      >
    </b-button>
    <div class="form-note text-center">
      Že imate račun? <NuxtLink to="/prijava">
        Prijavite se.
      </NuxtLink>
    </div>
  </form>
</template>

<script>
export default {
  data () {
    return {
      form: {
        username: '',
        email: '',
        phone: '',
        password: ''
      },
      errorUsername: false,
      errorEmail: false,
      errorPhone: false,
      errorPassword: false,
      errorRegister: false
    }
  },
  methods: {
    checkUsername () {
      this.errorUsername = this.form.username.length === 0
    },
    checkEmail () {
      this.errorEmail = this.form.email.length === 0
    },
    checkPhone () {
      this.errorPhone = this.form.phone.length === 0
    },
    checkPassword () {
      this.errorPassword = this.form.password.length === 0
    },
    async register (event) {
      try {
        await this.$store.dispatch('register', { form: this.form })
        await this.$router.push('login')
      } catch (err) {
        this.errorRegister = true
        console.log(err)
      }
    }
  }
}
</script>

<style>

</style>
