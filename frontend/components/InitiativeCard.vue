<template>
  <div class="initiative-card h-100" @click="openInitiative">
    <img
      v-if="cover_image"
      class="cover-image"
      :src="cover_image.image"
      alt=""
    >
    <div class="initiative-card-body">
      <h4>
        {{ title }}
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
            v-if="!has_voted"
            class="d-flex align-items-center"
            @click.stop="vote"
          >
            <LikeIcon class="mr-1" />
            <span>Podpri</span>
          </b-button>
          <b-button
            v-if="has_voted"
            class="d-flex align-items-center"
            @click.stop="removeVote"
          >
            <LikeIcon class="mr-1" />
            <span>Glas oddan!</span>
          </b-button>
          <span class="ml-1">{{ vote_count }}</span>
        </div>
        <div class="d-inline-flex align-items-center">
          <NuxtLink :to="`/predlogi/${id}`" class="btn d-flex align-items-center">
            <CommentIcon class="mr-1" />
            Komentiraj
          </NuxtLink>
          <span class="ml-1">{{ comment_count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CommentIcon from '~/assets/img/icons/comment.svg?inline'
import LikeIcon from '~/assets/img/icons/like.svg?inline'

export default {
  name: 'InitiativeCard',
  components: { CommentIcon, LikeIcon },
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
    },
    removeVote () {
      this.$emit('removeVote')
    },
    openInitiative () {
      this.$router.push(`/predlogi/${this.id}`)
    }
  }
}
</script>

<style scoped lang="scss">

.initiative-card {
  box-shadow: 4px 4px 6px #d3d7df, -4px -4px 6px #ffffff;

  &:hover {
    background-color: white;
    cursor: pointer;
  }

  .cover-image {
    width: 100%;
    height: 8rem;
    object-fit: cover;
  }

  .initiative-card-body {
    padding: 0.75rem;

    h4 {
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
      z-index: 10;

      svg {
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
