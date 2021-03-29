<template>
  <b-container fluid>
    <b-row class="justify-content-center">
      <b-col cols="12" md="10" lg="6" class="position-relative">
        <div>
          <div
            class="form-top form-top-zm"
          />
          <div class="initiative-form">
            <h4>ZANIMA ME</h4>
            <p class="form-subtitle">
              Vprašajte, kar vas zanima.
            </p>
            <Initiative
              :descriptions="descriptions"
              :error-draft="errorDraft"
              @create-initiative="createInitiative"
              @create-draft="createDraft"
            />
          </div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Initiative from '~/components/forms/InitiativeForm'

export default {
  components: { Initiative },
  middleware: 'auth',
  data () {
    return {
      type: 'ZM',
      descriptions: [
        'Kaj vas zanima? Vaše vprašanje naj bo jasno in nedvoumno; če je potrebno in če je mogoče, na kratko opišite okoliščine, na katere se nanaša vaše vprašanje. Tako vam bomo lažje podali kvaliteten in konkreten odgovor.'
      ],
      errorDraft: false
    }
  },
  computed: {
  },
  methods: {
    async createDraft (form, id) {
      this.errorDraft = false
      try {
        // is draft
        form.is_draft = true
        console.log('draft', form)
        if (id < 0) { // draft does not exist yet
          // add initiative type
          form.type = this.type
          id = await this.$store.dispatch('postInitiative', form)
        } else {
          id = await this.$store.dispatch('patchInitiative', { form, id })
        }
        if (id < 0) {
          this.errorDraft = true
          console.log('error create draft')
        } else {
          await this.$router.push('/')
        }
      } catch (err) {
        // this.errorComment = true
        console.log(err)
      }
    },
    async createInitiative (form, id) {
      try {
        // is draft
        form.is_draft = false
        // add initiative type
        form.type = this.type
        console.log('publish', form)
        if (id < 0) { // draft does not exist yet
          id = await this.$store.dispatch('postInitiative', form)
        } else {
          id = await this.$store.dispatch('patchInitiative', { form, id })
        }
        if (id < 0) {
          this.errorDraft = true
        } else {
          await this.$router.push(`/predlogi/${id}`)
        }
      } catch (err) {
        // this.errorComment = true
        console.log(err)
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>
