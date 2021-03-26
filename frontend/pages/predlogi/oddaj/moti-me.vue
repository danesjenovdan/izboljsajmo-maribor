<template>
  <b-container fluid>
    <b-row class="justify-content-center">
      <b-col cols="12" md="10" lg="6" class="position-relative">
        <div>
          <div
            class="form-top form-top-mm"
          />
          <div class="initiative-form">
            <h4>MOTI ME</h4>
            <p class="form-subtitle">
              Sporočite nam, če ste v svojem okolju zaznali kaj, kar vas moti (okvare, poškodbe, pomanjkljivosti, nepravilnosti …) in menite, da je v pristojnosti MO Maribor, da to reši.
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
      type: 'MM',
      descriptions: [
        'Na kratko opišite, kaj vas moti. Zakaj? Če je mogoče, opišite svojo izkušnje, da nam pomagate bolje razumeti vašo pripombo.',
        'Kako bi lahko to, kar vas moti, popravili?'
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
