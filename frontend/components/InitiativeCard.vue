<template>
  <div class="initiative-card h-100">
    <img
      v-if="cover_image"
      class="cover-image"
      :src="cover_image.image"
      alt=""
    >
    <div class="initiative-card-body">
      <h4>
        <NuxtLink :to="`/predlogi/${id}`">
          {{ title }}
        </NuxtLink>
      </h4>
      <span class="author">{{ author }}</span>
      <div class="my-1">
        <span class="tag">{{ status }}</span>
        <span class="tag">{{ area.name }}</span>
        <span class="tag">{{ date(created) }}</span>
      </div>
      <p>
        {{ description }}
      </p>
      <hr class="hr-upper">
      <hr class="hr-lower">
      <div class="d-flex justify-content-between">
        <div class="d-inline-flex align-items-center">
          <b-button
            class="d-flex align-items-center"
            :disabled="has_voted"
            @click="vote"
          >
            <img
              src="~/assets/img/icons/love.svg"
              alt="love"
              class="mr-1"
            >
            <span v-if="!has_voted">Podpri</span>
            <span v-if="has_voted">Glas oddan!</span>
          </b-button>
          <span class="ml-1">{{ vote_count }}</span>
        </div>
        <div class="d-inline-flex align-items-center">
          <NuxtLink :to="`/predlogi/${id}`" class="btn d-flex align-items-center">
            <img
              src="~/assets/img/icons/comment.svg"
              alt="comment"
              class="mr-1"
            >
            Komentiraj
          </NuxtLink>
          <span class="ml-1">{{ comment_count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InitiativeCard',
  props: {
    id: {
      type: Number,
      default: -1
    },
    title: {
      type: String,
      default: ''
    },
    author: {
      type: String,
      default: ''
    },
    status: {
      type: String,
      default: ''
    },
    area: {
      type: Object,
      default: null
    },
    created: {
      type: String,
      default: null
    },
    cover_image: {
      type: Object,
      default: null
    },
    description: {
      type: String,
      default: ''
    },
    vote_count: {
      type: Number,
      default: -1
    },
    has_voted: Boolean,
    comment_count: {
      type: Number,
      default: -1
    }
  },
  data () {
    return {
    }
  },
  methods: {
    date (date) {
      const d = new Date(date)
      return `${d.getDate()}.${d.getMonth() + 1}.${d.getFullYear()}`
    },
    vote () {
      this.$emit('vote')
    }
  }
}
</script>

<style scoped lang="scss">

h4 {
  font-weight: 600;
}

.initiative-card {
  box-shadow: 4px 4px 6px #d3d7df, -4px -4px 6px #ffffff;

  .cover-image {
    width: 100%;
    height: 8rem;
    object-fit: cover;
  }

  .initiative-card-body {
    padding: 0.5rem;

    h4 a {
      color: black;
      line-height: 1;
      font-weight: 700;
    }

    .author {
      font-size: 0.9rem;
      font-style: italic;
    }

    .tag {
      background-color: #eff3fb;
      border-radius: 0.5rem;
      padding: 0.25rem;
      font-size: 0.75rem;
    }

    p {
      font-size: 0.9rem;
    }

    .btn {
      margin: 0;
      padding: 0.25rem 0.5rem;
      font-style: normal;
      font-size: 0.75rem;
      font-weight: 400;
      letter-spacing: normal;

      img {
        height: 0.8rem;
      }
    }

    hr {
      &.hr-upper {
         margin-top: 1rem
      }
      &.hr-lower {
         margin-bottom: 1rem;
      }
    }
  }
}

</style>
