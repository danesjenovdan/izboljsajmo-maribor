<template>
  <b-form @submit.prevent="login">
    <div class="form-group">
      <label for="username">E-naslov ali uporabniško ime</label>
      <span v-if="errorUsername" class="error-message">Vpišite uporabniško ime.</span>
      <b-form-input
        id="username"
        v-model.trim="form.username"
        :class="{ 'error-input': errorUsername }"
        name="username"
        type="text"
        required
        @keyup="checkUsername"
      />
    </div>
    <div class="form-group position-relative">
      <label for="password">Geslo</label>
      <span v-if="errorPassword" class="error-message">Vpišite geslo.</span>
      <b-form-input
        id="password"
        v-model.trim="form.password"
        :class="{ 'error-input': errorPassword }"
        name="password"
        :type="passwordVisibility ? 'text' : 'password'"
        required
        @keyup="checkPassword"
      />
      <span class="position-absolute password-button" @click="passwordVisibility = !passwordVisibility">
        <EyeHideIcon v-if="passwordVisibility" />
        <EyeShowIcon v-if="!passwordVisibility" />
      </span>
    </div>
    <div class="text-right mt-2">
      <a class="back-button" href="/pozabljeno-geslo">Pozabljeno geslo?</a>
    </div>
    <b-form-group id="remember-me-input-group" v-slot="{ ariaDescribedby }">
      <b-form-checkbox
        id="remember-me"
        v-model="rememberMe"
        :aria-describedby="ariaDescribedby"
      >
        Zapomni si me.
      </b-form-checkbox>
    </b-form-group>
    <p v-if="errorLogin" class="message error d-flex justify-content-center align-items-center position-relative">
      <IconDanger /><span v-if="errorMessage">{{ errorMessage }}</span><span v-else>Prijava ni uspela.</span>
      <span class="clickable position-absolute" @click="closeErrorMessage">Zapri</span>
    </p>
    <b-button type="submit" class="w-100 d-flex justify-content-center align-items-center position-relative">
      VSTOPI
      <ArrowRightIcon class="position-absolute" />
    </b-button>
    <div class="form-note text-center">
      Nimate računa? <NuxtLink class="back-button" to="/registracija">
        Registrirajte se
      </NuxtLink>
    </div>
  </b-form>
</template>

<script>
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'
import IconDanger from '~/assets/img/icons/danger.svg?inline'
import EyeShowIcon from '~/assets/img/icons/eye-show.svg?inline'
import EyeHideIcon from '~/assets/img/icons/eye-hide.svg?inline'

export default {
  components: { ArrowRightIcon, IconDanger, EyeShowIcon, EyeHideIcon },
  data () {
    return {
      rememberMe: false,
      form: {
        username: '',
        password: ''
      },
      passwordVisibility: false,
      errorUsername: false,
      errorPassword: false,
      errorLogin: false,
      errorMessage: ""
    }
  },
  methods: {
    checkUsername () {
      this.errorUsername = this.form.username.length === 0
    },
    checkPassword () {
      this.errorPassword = this.form.password.length === 0
    },
    async login (event) {
      const response = await this.$store.dispatch('login', { form: this.form })
      
      if (!response.success) {
        this.errorLogin = true
        this.errorMessage = response.message
      }
    },
    closeErrorMessage () {
      this.errorLogin = false
    }
  }
}
</script>

<style lang="scss">

#remember-me-input-group {
  .custom-checkbox label.custom-control-label:before, .custom-checkbox label.custom-control-label:after {
    border: none;
    box-shadow: 3px 3px 4px rgba(208, 212, 220, 0.35), -3px -3px 4px #ffffff, inset 0 3px 4px rgba(208, 212, 220, 0.5);
  }
}

</style>
