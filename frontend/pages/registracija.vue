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
import Register from '~/components/forms/Register'
import RegisterOrganization from '~/components/forms/RegisterOrganization'

export default {
  components: { Register, RegisterOrganization },
  layout: 'login',
  data () {
    return {
      registrationForm: 'posameznik'
    }
  }
}
</script>
