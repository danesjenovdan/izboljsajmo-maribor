<template>
  <b-form @submit.prevent="onSubmit">
    <b-form-group
      id="username-input-group"
      label="E-naslov ali uporabniško ime"
      label-for="username"
    >
      <b-form-input
        id="username"
        v-model="form.email"
        name="username"
        type="text"
        required
      />
    </b-form-group>
    <b-form-group
      id="password-input-group"
      label="Geslo"
      label-for="password"
    >
      <b-form-input
        id="password"
        v-model="form.password"
        name="password"
        type="password"
        required
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
        email: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit (event) {
      alert(JSON.stringify(this.form))
    }
  }
}
</script>

<style>

</style>
