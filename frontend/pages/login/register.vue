<template>
  <div>
    <h1>Registriraj se!</h1>
    <b-form-group v-slot="{ ariaDescribedby }">
      <b-form-radio v-model="registrationForm" :aria-describedby="ariaDescribedby" value="posameznik">
        Sem posameznik/-ca.
      </b-form-radio>
      <b-form-radio v-model="registrationForm" :aria-describedby="ariaDescribedby" value="organizacija">
        Zastopam skupino ali organizacijo.
      </b-form-radio>
    </b-form-group>
    <hr class="hr-upper">
    <hr class="hr-lower">
    <div v-if="registrationForm === 'posameznik'">
      <Register />
    </div>
    <div v-else>
      <RegisterOrganization />
    </div>
  </div>
</template>

<script>
export default {
  layout: 'login',
  data () {
    return {
      registrationForm: 'posameznik',
      form: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit (event) {
      event.preventDefault()
      alert(JSON.stringify(this.form))
    },
    onReset (event) {
      event.preventDefault()
      // Reset our form values
      this.form.email = ''
      this.form.password = ''
    }
  }
}
</script>
