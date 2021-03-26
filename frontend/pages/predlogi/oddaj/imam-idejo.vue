<template>
  <b-container fluid>
    <b-row class="justify-content-center">
      <b-col cols="12" md="10" lg="6" class="position-relative">
        <div>
          <div
            class="form-top form-top-ii"
          />
          <div class="initiative-form">
            <h4>IMAM IDEJO</h4>
            <p class="form-subtitle">
              Sporočite nam, če imate predlog za izboljšavo ali novost v svojem okolju.
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
      type: 'II',
      descriptions: [
        'Na kratko opišite svojo pobudo oziroma predlog? Zakaj ta predlog? Katere izzive /probleme, pomankljivosti, slabosti v skupnosti/ mestu bi z uresničitvijo  vaše pobude rešili?',
        'Kakšen je vaš idejni predlog rešitve, izzivov/problemov, uvedbe izboljšav, izkoriščanja priložnosti? Kaj konkretno predlagate?  Kakšne priložnosti naslavlja?  Kaj bi se z izvedbo vašega predloga izboljšalo? Ali predlog spodbuja povezovanje /sodelovanje ljudi? Krepi njihove sposobnosti za lažje samostojno reševanje izzivov v skupnosti/mestu?',
        'Kako in kje bi realizirali vašo pobudo-idejo? Katere aktivnosti (koraki /postopki, dela, opravila) so potrebni za izvedbo rešitve? Ali se lahko vaša pobuda realizira v nevladnem sektorju (v okviru društev, civilnih pobud ..), kot socialno podjetniški/zadružni/ podjetniški podjem, razvojni projekt v mestu ali kot gospodarski projekt/pobuda? Koga bi pritegnili k sodelovanju?',
        'Ali lahko ocenite vrednost realizacije projekta / ideje (v EUR)?'
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
