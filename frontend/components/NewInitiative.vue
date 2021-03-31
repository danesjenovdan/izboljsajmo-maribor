<template>
  <b-container fluid>
    <b-row class="justify-content-center">
      <b-col cols="12" md="10" lg="6" class="position-relative">
        <div>
          <div
            class="form-top"
            :class="`form-top-${type}`"
          />
          <div class="initiative-form">
            <h4>{{ title }}</h4>
            <p class="form-subtitle">
              {{ subtitle }}
            </p>
            <Initiative
              :descriptions="descriptions"
              :error-message="errorMessage"
              :error-message-text="errorMessageText"
              :success-message="successMessage"
              :success-message-text="successMessageText"
              @create-initiative="createInitiative"
              @create-draft="createDraft"
              @delete-initiative="deleteInitiative"
              @close-error-message="errorMessage = false"
              @close-success-message="successMessage = false"
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
  props: {
    title: {
      type: String,
      default: ''
    },
    subtitle: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'MM'
    },
    descriptions: {
      type: Array
    }
  },
  data () {
    return {
      errorMessage: false,
      errorMessageText: 'Prišlo je do napake.',
      successMessage: false,
      successMessageText: ''
    }
  },
  computed: {
  },
  methods: {
    async createDraft (form, id) {
      this.errorMessage = false
      try {
        // is draft
        form.is_draft = true
        console.log('draft', form)
        if (id < 0) { // draft does not exist yet
          // add initiative type
          form.type = this.type
          await this.$store.dispatch('postInitiative', form)
        } else {
          await this.$store.dispatch('patchInitiative', { form, id })
        }
        this.errorMessage = false
        this.successMessage = true
        this.successMessageText = 'Vaša pobuda je bila uspešno shranjena v vaš profil.'
      } catch (err) {
        console.log(err)
        this.errorMessage = true
        this.successMessage = false
      }
    },
    async createInitiative (form, id) {
      this.errorMessage = false
      try {
        // is draft
        form.is_draft = false
        // add initiative type
        form.type = this.type
        console.log('publish', form)
        if (id < 0) { // draft does not exist yet
          await this.$store.dispatch('postInitiative', form)
        } else {
          await this.$store.dispatch('patchInitiative', { form, id })
        }
        this.errorMessage = false
        this.successMessage = true
        this.successMessageText = 'Vaša pobuda je bila uspešno shranjena v vaš profil.'
      } catch (err) {
        console.log(err)
        this.errorMessage = true
        this.successMessage = false
      }
    },
    async deleteInitiative (id) {
      this.errorMessage = false
      try {
        if (id >= 0) { // delete initiative from db
          const res = await this.$store.dispatch('deleteInitiative', {
            id
          })
        }
        this.errorMessage = false
        this.successMessage = true
        this.successMessageText = 'Vaša pobuda je bila izbrisana.'
      } catch (err) {
        console.log(err)
        this.errorMessage = true
        this.successMessage = false
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>