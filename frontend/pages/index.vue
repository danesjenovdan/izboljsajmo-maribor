<template>
  <b-container fluid>
    <b-row class="p-4">
      <b-col cols="12" lg="3" class="text-center text-lg-left mb-4">
        <h1>Pozdravljeni, Janez Novak</h1>
        <b-button
          class="logout-button w-75 position-relative d-inline-flex justify-content-center"
          @click="logout"
        >
          ODJAVA
          <img src="~/assets/img/icons/exit-right.png" alt="logout icon" class="position-absolute">
        </b-button>
      </b-col>
      <b-col cols="12" lg="9">
        <b-row class="card-outline p-4 mb-4">
          <b-col cols="12" md="4" lg="2" class="mb-4">
            <h4>Neoddani predlogi</h4>
          </b-col>
          <b-col cols="12" md="8" lg="10">
            <b-row>
              <b-col
                v-for="draft in drafts"
                :key="draft.title"
                cols="12"
                lg="6"
                xl="4"
                class="mb-4"
              >
                <div class="initiative-card draft h-100">
                  <img
                    class="cover-image"
                    :src="$axios.defaults.baseURL + draft.cover_image.image"
                    alt="Initiative draft cover image"
                  >
                  <div class="initiative-card-body">
                    <h4>{{ draft.title }}</h4>
                    <p>{{ draft.description }}</p>
                    <div class="d-flex justify-content-center">
                      <div class="d-inline-flex align-items-center">
                        <b-button class="d-flex align-items-center position-relative">
                          <span class="text-uppercase pr-2">Uredi</span>
                          <img
                            src="~/assets/img/icons/edit.png"
                            alt="edit icon"
                            class="position-absolute"
                          >
                        </b-button>
                      </div>
                    </div>
                  </div>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <b-row class="card-outline p-4 mb-4">
          <b-col cols="12" md="4" lg="2" class="mb-4">
            <h4>Oddani predlogi</h4>
          </b-col>
          <b-col cols="12" md="8" lg="10">
            <b-row>
              <b-col
                v-for="initiative in published"
                :key="initiative.created"
                cols="12"
                lg="6"
                xl="4"
                class="mb-4"
              >
                <div class="initiative-card published h-100">
                  <img
                    class="cover-image"
                    :src="$axios.defaults.baseURL + initiative.cover_image.image"
                    alt="Initiative cover image"
                  >
                  <div class="initiative-card-body">
                    <h4>
                      <NuxtLink :to="`/predlogi/${initiative.id}`">
                        {{ initiative.title }}
                      </NuxtLink>
                    </h4>
                    <span class="author">{{ initiative.author }}</span>
                    <div class="my-1">
                      <span class="tag">Slišimo</span>
                      <span class="tag">Promet</span>
                      <span class="tag">{{ date(initiative.created) }}</span>
                    </div>
                    <p> {{ initiative.description }}</p>
                    <hr class="hr-upper">
                    <hr class="hr-lower">
                    <div class="d-flex justify-content-between">
                      <div class="d-inline-flex align-items-center">
                        <b-button class="d-flex align-items-center">
                          <img
                            src="~/assets/img/icons/love.png"
                            alt="love"
                            class="mr-1"
                          >
                          Podpri
                        </b-button>
                        <span class="ml-1">{{ initiative.vote_count }}</span>
                      </div>
                      <div class="d-inline-flex align-items-center">
                        <b-button class="d-flex align-items-center">
                          <img
                            src="~/assets/img/icons/comment.png"
                            alt="comment"
                            class="mr-1"
                          >
                          Komentiraj
                        </b-button>
                        <span class="ml-1">{{ initiative.comment_count }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  middleware: 'auth',
  asyncData ({ store, $axios, redirect }) {
    return $axios.get('v1/initiatives/my', {
      headers: {
        Authorization: 'Bearer ' + store.getters.token
      }
    })
      .then((res) => {
        return {
          drafts: res.data.drafts,
          published: res.data.published
        }
      })
      .catch((e) => {
        return redirect('/404')
      // console.log(params)
      })
  },
  data () {
    return {
      drafts: [],
      published: []
    }
  },
  methods: {
    date (date) {
      const d = new Date(date)
      return `${d.getDate()}.${d.getMonth() + 1}.${d.getFullYear()}`
    },
    async logout () {
      await this.$store.dispatch('logout')
      await this.$router.push('/predlogi')
    }
  }
}
</script>

<style scoped lang="scss">

h1, h4 {
  font-weight: 700;
}

.logout-button {
  background-color: #d7d7d7;
  &:hover {
    background-color: #6c757d;
  }

  img {
    right: 0.5rem;
    height: 1.5rem;
  }
}

.card-outline {
  box-shadow: 4px 4px 11px #d4d9e1, -5px -5px 11px #ffffff;
  border-radius: 0.5rem;
}

.initiative-card {
  box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;

  .cover-image {
    width: 100%;
    height: 8rem;
    object-fit: cover;
  }

  .initiative-card-body {
    padding: 0.75rem;

    h4 a {
      color: black;
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

    hr {
      &.hr-upper {
        margin-top: 1rem
      }
      &.hr-lower {
        margin-bottom: 1rem;
      }
    }
  }

  &.draft {
    .btn {
      padding: 0.75rem 3rem;

      img {
        height: 1.5rem;
        right: 0.75rem;
      }
    }
  }

  &.published {
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
  }
}

</style>
