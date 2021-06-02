<template>
  <form @submit.prevent="register">
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
    <div class="form-group position-relative">
      <label for="password">Geslo</label>
      <span v-if="errorPassword" class="error-message">Vpišite geslo.</span>
      <b-form-input
        id="password"
        v-model="form.password"
        :class="{ 'error-input': errorPassword }"
        :type="passwordVisibility ? 'text' : 'password'"
        required
        @keyup="checkPassword"
      />
      <span class="position-absolute password-button" @click="passwordVisibility = !passwordVisibility">
        <EyeHideIcon v-if="passwordVisibility" />
        <EyeShowIcon v-if="!passwordVisibility" />
      </span>
    </div>
    <p v-if="errorRegister" class="message error d-flex justify-content-center align-items-center position-relative">
      <IconDanger />Registracija ni uspela.
      <span class="position-absolute" @click="errorRegister = false">Zapri</span>
    </p>
    <p v-if="success" class="message success d-flex justify-content-center align-items-center position-relative">
      <IconSuccess />Registracija uspešna! Prosimo, potrdite račun s klikom na povezavo, ki ste jo prejeli na svoj e-naslov.
      <span class="position-absolute" @click="success = false">Zapri</span>
    </p>
    <b-button type="submit" class="w-100 d-flex justify-content-center align-items-center position-relative">
      ZAKLJUČI REGISTRACIJO
      <ArrowRightIcon class="position-absolute" />
    </b-button>
    <div class="form-note text-center">
      Že imate račun? <NuxtLink class="back-button" to="/prijava">
        Prijavite se.
      </NuxtLink>
    </div>
  </form>
</template>

<script>
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'
import IconDanger from '~/assets/img/icons/danger.svg?inline'
import IconSuccess from '~/assets/img/icons/success.svg?inline'
import EyeShowIcon from '~/assets/img/icons/eye-show.svg?inline'
import EyeHideIcon from '~/assets/img/icons/eye-hide.svg?inline'

export default {
  components: { ArrowRightIcon, IconSuccess, IconDanger, EyeShowIcon, EyeHideIcon },
  data () {
    return {
      form: {
        username: '',
        email: '',
        phone: '',
        password: ''
      },
      passwordVisibility: false,
      errorUsername: false,
      errorEmail: false,
      errorPhone: false,
      errorPassword: false,
      errorRegister: false,
      success: false
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
    emptyForm () {
      this.form.username = ''
      this.form.email = ''
      this.form.phone = ''
      this.form.password = ''
    },
    async register (event) {
      try {
        await this.$store.dispatch('register', { form: this.form })
        this.emptyForm()
        this.success = true
        // await this.$router.push('login')
      } catch (err) {
        this.errorRegister = true
      }
    }
  }
}
</script>

<style>

</style>
