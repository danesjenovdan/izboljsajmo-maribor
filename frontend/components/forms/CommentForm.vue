<template>
  <b-form @submit.prevent="postComment">
    <h5>Oddaj komentar</h5>
    <p>Komentarji so zaradi zagotavljanja višjih standardov razprave skladno s pravili pred objavo moderirani.</p>
    <b-form-textarea
      id="comment"
      v-model="content"
      placeholder="Napiši komentar"
      rows="5"
      max-rows="10"
      @change="checkComment"
    />
    <p v-if="errorComment" class="message error d-flex justify-content-center position-relative">
      <IconDanger />Komentar ne more biti prazen.
      <span class="position-absolute" @click="errorComment = false">Zapri</span>
    </p>
    <p v-if="errorMessage" class="message error d-flex justify-content-center position-relative">
      <IconDanger />{{ errorMessageText }}
      <span class="position-absolute" @click="errorMessage = false">Zapri</span>
    </p>
    <p v-if="successMessage" class="message success d-flex justify-content-center position-relative">
      <IconSuccess />Vaš komentar je bil uspešno oddan.
      <span class="position-absolute" @click="successMessage = false">Zapri</span>
    </p>
    <div class="d-flex justify-content-end">
      <b-button type="submit" class="d-inline-flex align-items-center">
        <span>KOMENTIRAJ</span>
        <ArrowRightIcon />
      </b-button>
    </div>
  </b-form>
</template>

<script>
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'
import IconDanger from '~/assets/img/icons/danger.svg?inline'
import IconSuccess from '~/assets/img/icons/success.svg?inline'

export default {
  components: { ArrowRightIcon, IconDanger, IconSuccess },
  props: {
    id: String
  },
  data () {
    return {
      content: '',
      errorComment: false,
      errorMessage: false,
      errorMessageText: '',
      successMessage: false
    }
  },
  computed: {
  },
  methods: {
    async postComment () {
      this.checkComment()
      if (!this.errorComment) {
        if (this.$auth.loggedIn) {
          try {
            await this.$store.dispatch('postComment', { content: this.content, id: this.id })
            this.successMessage = true
            this.content = ''
          } catch (err) {
            this.errorMessage = true
            this.errorMessageText = 'Prišlo je do napake.'
          }
        } else {
          this.errorMessage = true
          this.errorMessageText = 'Če želite oddati komentar, se morate najprej vpisati.'
        }
      }
    },
    checkComment () {
      this.errorComment = this.content.length <= 0
    }
  }
}
</script>

<style scoped lang="scss">

#comment {
  overflow: hidden !important;
}

h5 {
  font-weight: 600;
}

button {
  padding: 0.5rem 1rem;

   svg {
    height: 1.2rem;
    margin-left: 0.5rem;
  }
}

</style>
