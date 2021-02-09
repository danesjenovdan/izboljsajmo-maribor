<template>
  <b-form @submit.prevent="register">
    <p v-if="errorRegister" class="error-message text-center mt-4">
      Registracija ni uspela.
    </p>
    <b-form-group
      id="username-input-group"
      label="Ime skupine ali organizacije (uporabniško ime)"
      label-for="username"
      :class="{ 'error-message': errorUsername }"
    >
      <b-form-input
        id="username"
        v-model="form.username"
        type="text"
        required
        @blur="checkUsername"
      />
    </b-form-group>
    <b-form-group
      id="name-input-group"
      label="Ime in priimek odgovorne osebe"
      label-for="name"
      :class="{ 'error-message': errorName }"
    >
      <b-form-input
        id="name"
        v-model="form.name"
        type="text"
        required
        @blur="checkName"
      />
    </b-form-group>
    <b-form-group
      id="members-input-group"
      label="Število oseb v skupini ali število organizacij"
      label-for="no-of-members"
      :class="{ 'error-message': errorMembers }"
    >
      <b-form-input
        id="no-of-members"
        v-model="form.membersNumber"
        type="number"
        min="1"
        required
        @blur="checkMembers"
      />
    </b-form-group>
    <b-form-group
      id="email-input-group"
      label="E-naslov"
      label-for="email"
      :class="{ 'error-message': errorEmail }"
    >
      <b-form-input
        id="email"
        v-model="form.email"
        type="email"
        required
        @blur="checkEmail"
      />
    </b-form-group>
    <b-form-group
      id="phone-input-group"
      label="Telefonska številka"
      label-for="phone"
      :class="{ 'error-message': errorPhone }"
    >
      <b-form-input
        id="phone"
        v-model="form.phone"
        type="tel"
        required
        @blur="checkPhone"
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
        v-model="form.password"
        type="password"
        required
        @blur="checkPassword"
      />
    </b-form-group>
    <b-button type="submit" class="w-100">
      ZAKLJUČI REGISTRACIJO<span class="float-right"><img src="~/assets/img/icons/arrow-right.png"></span>
    </b-button>
    <div class="form-note text-center">
      Že imaš račun? <NuxtLink to="/login">Prijavi se</NuxtLink>
    </div>
  </b-form>
</template>

<script>
export default {
  data () {
    return {
      form: {
        username: '',
        name: '',
        membersNumber: 1,
        email: '',
        phone: '',
        password: ''
      },
      errorUsername: false,
      errorName: false,
      errorMembers: false,
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
    checkName () {
      this.errorName = this.form.name.length === 0
    },
    checkMembers () {},
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
      alert(JSON.stringify(this.form))
      try {
        await this.$store.dispatch('registerOrganization', { form: this.form })
        await this.$router.push('/login')
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
