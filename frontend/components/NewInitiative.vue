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
              :has-social-innovative-idea-checkbox="hasSocialInnovativeIdeaCheckbox"
              @create-initiative="createInitiative"
              @create-draft="createDraft"
              @delete-initiative="deleteInitiative"
              @on-error="onError"
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
    }
  },
  data () {
    return {
      errorMessage: false,
      errorMessageText: 'Prišlo je do napake.',
      successMessage: false,
      successMessageText: '',
      descriptions: [],
      hasSocialInnovativeIdeaCheckbox: this.type === 'II'
    }
  },
  async created () {
    this.descriptions = await this.$store.dispatch('getDescriptionDefinitions', { type: this.type })
  },
  methods: {
    onError () {
      this.errorMessage = true
      this.errorMessageText = 'Prišlo je do napake.'
    },
    async createDraft (form, id) {
      this.errorMessage = false
      try {
        // is draft
        form.is_draft = true
        if (id < 0) { // draft does not exist yet
          // add initiative type
          form.type = this.type
          await this.$store.dispatch('postInitiative', form)
        } else {
          await this.$store.dispatch('patchInitiative', { form, id })
        }
        this.errorMessage = false
        this.successMessage = true
        this.successMessageText = 'Vaša pobuda je bila uspešno shranjena.'
      } catch (err) {
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
        if (id < 0) { // draft does not exist yet
          await this.$store.dispatch('postInitiative', form)
        } else {
          await this.$store.dispatch('patchInitiative', { form, id })
        }
        this.errorMessage = false
        this.successMessage = true
        this.successMessageText = 'Vaša pobuda je bila uspešno oddana.'
      } catch (err) {
        this.errorMessage = true
        this.successMessage = false
      }
    },
    async deleteInitiative (id) {
      this.errorMessage = false
      try {
        if (id >= 0) { // delete initiative from db
          await this.$store.dispatch('deleteInitiative', {
            id
          })
        }
        await this.$router.push('/profil')
      } catch (err) {
        this.errorMessage = true
        this.successMessage = false
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>
