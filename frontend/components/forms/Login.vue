<template>
  <b-form @submit.prevent="login">
    <p v-if="errorLogin" class="error-message text-center mt-4">
      Prijava ni uspela.
    </p>
    <b-form-group
      id="username-input-group"
      label="E-naslov ali uporabniško ime"
      label-for="username"
      :class="{ 'error-message': errorUsername }"
    >
      <b-form-input
        id="username"
        v-model.trim="form.username"
        name="username"
        type="text"
        required
        @blur="checkUsername"
      />
    </b-form-group>
    <b-form-group
      id="password-input-group"
      label="Geslo"
      label-for="password"
      :class="{ 'error-message': errorPassword }"
    >
      <b-form-input
        id="password"
        v-model.trim="form.password"
        name="password"
        type="password"
        required
        @blur="checkPassword"
      />
    </b-form-group>
    <div class="text-right">
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
      <b-button type="submit" class="w-100">
        VSTOPI<span class="float-right"><img src="~/assets/img/icons/arrow-right.png"></span>
      </b-button>
      <div class="form-note text-center">
        Nimaš računa? <a href="/login/register">Registriraj se</a>
      </div>
    </b-form-group>
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
        await this.$router.push('/')
      } catch (err) {
        this.errorLogin = true
        console.log(err)
      }
    }
  }
}
</script>

<style>

</style>
