<template>
  <b-form @submit.prevent="register">
    <div class="form-group">
      <label for="username">Ime skupine ali organizacije (uporabniško ime)</label>
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
      <label for="name">Ime in priimek odgovorne osebe</label>
      <span v-if="errorName" class="error-message">Vpišite ime in priimek.</span>
      <b-form-input
        id="name"
        v-model="form.name"
        :class="{ 'error-input': errorName }"
        name="name"
        type="text"
        required
        @keyup="checkName"
      />
    </div>
    <div class="form-group">
      <label for="no-of-members">Število oseb v skupini ali število organizacij</label>
      <span v-if="errorMembers" class="error-message">Vpišite število oseb.</span>
      <b-form-input
        id="no-of-members"
        v-model="form.membersNumber"
        :class="{ 'error-input': errorMembers }"
        type="number"
        min="1"
        required
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
  </b-form>
</template>

<script>
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'
import IconDanger from '~/assets/img/icons/danger.svg?inline'
import IconSuccess from '~/assets/img/icons/success.svg?inline'
import EyeShowIcon from '~/assets/img/icons/eye-show.svg?inline'
import EyeHideIcon from '~/assets/img/icons/eye-hide.svg?inline'

export default {
  components: { ArrowRightIcon, IconDanger, IconSuccess, EyeShowIcon, EyeHideIcon },
  data () {
    return {
      form: {
        username: '',
        name: '',
        membersNumber: null,
        email: '',
        phone: '',
        password: ''
      },
      passwordVisibility: false,
      errorUsername: false,
      errorName: false,
      errorMembers: false,
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
    checkName () {
      this.errorName = this.form.name.length === 0
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
      this.form.name = ''
      this.form.membersNumber = null
      this.form.email = ''
      this.form.phone = ''
      this.form.password = ''
    },
    async register (event) {
      try {
        await this.$store.dispatch('registerOrganization', { form: this.form })
        this.emptyForm()
        this.success = true
        // await this.$router.push('/login')
      } catch (err) {
        this.errorRegister = true
      }
    }
  }
}
</script>

<style>

</style>
