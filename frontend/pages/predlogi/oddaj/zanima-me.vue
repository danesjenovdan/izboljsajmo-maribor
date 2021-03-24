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
      initiativeType: 'ZM',
      descriptions: [
        'Kaj vas zanima? Vaše vprašanje naj bo jasno in nedvoumno; če je potrebno in če je mogoče, na kratko opišite okoliščine, na katere se nanaša vaše vprašanje. Tako vam bomo lažje podali kvaliteten in konkreten odgovor.'
      ]
    }
  },
  computed: {
  },
  methods: {
    async createDraft (form) {
      try {
        // is draft
        form.isDraft = true
        // add initiative type
        form.initiativeType = this.initiativeType
        console.log('draft', form)
        await this.$store.dispatch('postInitiative', form)
        await this.$router.push('/')
      } catch (err) {
        // this.errorComment = true
        console.log(err)
      }
    },
    async createInitiative (form) {
      try {
        // add initiative type
        form.initiativeType = this.initiativeType
        console.log('publish', form)
        const id = await this.$store.dispatch('postInitiative', form)
        await this.$router.push(`/predlogi/${id}`)
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
