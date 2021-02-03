<template>
  <b-form @submit="onSubmit">
    <b-form-group
      id="username-input-group"
      label="Ime skupine ali organizacije (uporabniško ime)"
      label-for="name"
    >
      <b-form-input
        id="username"
        v-model="form.username"
        type="text"
        required
      />
    </b-form-group>
    <b-form-group
      id="name-input-group"
      label="Ime in priimek odgovorne osebe"
      label-for="name"
    >
      <b-form-input
        id="name"
        v-model="form.name"
        type="text"
        required
      />
    </b-form-group>
    <b-form-group
      id="members-input-group"
      label="Število oseb v skupini ali število organizacij"
      label-for="no-of-members"
    >
      <b-form-input
        id="no-of-members"
        v-model="form.membersNumber"
        type="number"
        min="1"
        required
      />
    </b-form-group>
    <b-form-group
      id="email-input-group"
      label="E-naslov"
      label-for="email"
    >
      <b-form-input
        id="email"
        v-model="form.email"
        type="email"
        required
      />
    </b-form-group>
    <b-form-group
      id="phone-input-group"
      label="Telefonska številka"
      label-for="phone"
    >
      <b-form-input
        id="phone"
        v-model="form.phone"
        type="tel"
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
        type="password"
        required
      />
    </b-form-group>
    <b-button type="submit" class="w-100">
      ZAKLJUČI REGISTRACIJO<span class="float-right"><img src="~/assets/img/icons/arrow-right.png"></span>
    </b-button>
    <div class="form-note text-center">
      Že imaš račun? <a href="/login">Prijavi se</a>
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
