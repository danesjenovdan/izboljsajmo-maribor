<template>
  <b-form @submit.prevent="login">
    <p v-if="errorLogin" class="error-message text-center mt-4">
      Prijava ni uspela.
    </p>
    <div class="form-group">
      <label for="username">E-naslov ali uporabniško ime</label>
      <span v-if="errorUsername" class="error-message">Vpiši uporabniško ime.</span>
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
    <div class="form-group">
      <label for="password">Geslo</label>
      <span v-if="errorPassword" class="error-message">Vpiši geslo.</span>
      <b-form-input
        id="password"
        v-model.trim="form.password"
        :class="{ 'error-input': errorPassword }"
        name="password"
        type="password"
        required
        @keyup="checkPassword"
      />
    </div>
    <div class="text-right mt-2">
      <a href="/">Pozabljeno geslo?</a>
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
    <b-button type="submit" class="w-100">
      VSTOPI<span class="float-right"><img src="~/assets/img/icons/arrow-right.png"></span>
    </b-button>
    <div class="form-note text-center">
      Nimaš računa? <NuxtLink to="/registracija">
        Registriraj se
      </NuxtLink>
    </div>
  </b-form>
</template>

<script>

export default {
  data () {
    return {
      rememberMe: false,
      form: {
        username: '',
        password: ''
      },
      errorUsername: false,
      errorPassword: false,
      errorLogin: false
    }
  },
  computed: {
  },
  methods: {
    checkUsername () {
      this.errorUsername = this.form.username.length === 0
    },
    checkPassword () {
      this.errorPassword = this.form.password.length === 0
    },
    async login (event) {
      // console.log(JSON.stringify(this.form))
      try {
        await this.$store.dispatch('login', { form: this.form })
      } catch (err) {
        this.errorLogin = true
        console.log(err)
      }
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
