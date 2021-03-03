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
    ></b-form-textarea>
    <p v-if="errorComment" class="error-message">
      Komentar ne more biti prazen.
    </p>
    <div class="d-flex justify-content-end">
      <b-button type="submit" class="d-inline-flex align-items-center">
        <span>KOMENTIRAJ</span>
        <img src="~/assets/img/icons/arrow-right.png" alt="arrow right">
      </b-button>
    </div>
  </b-form>
</template>

<script>

export default {
  props: {
    id: String
  },
  data () {
    return {
      content: '',
      errorComment: false
    }
  },
  computed: {
  },
  methods: {
    async postComment () {
      if (this.content.length > 0) {
        try {
          await this.$store.dispatch('postComment', { content: this.content, id: this.id })
        } catch (err) {
          this.errorComment = true
          console.log(err)
        }
      } else {
        this.errorComment = true
      }
    },
    checkComment () {
      if (this.content.length > 0) {
        this.errorComment = false
      }
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

  img {
    height: 1.2rem;
    margin-left: 0.5rem;
  }
}

</style>
