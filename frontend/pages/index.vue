<template>
  <b-container fluid>
    <b-row class="p-4">
      <b-col cols="12" lg="3" class="text-center text-lg-left mb-4">
        <h1>Pozdravljeni, {{ this.$auth.user.username }}</h1>
        <b-button
          class="logout-button w-75 position-relative d-inline-flex justify-content-center"
          @click="logout"
        >
          ODJAVA
          <img src="~/assets/img/icons/exit-right.png" alt="logout icon" class="position-absolute">
        </b-button>
      </b-col>
      <b-col cols="12" lg="9">
        <b-row v-if="drafts.length > 0" class="card-outline p-4 mb-4">
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
                    :src="draft.cover_image.image"
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
            <p v-if="published.length === 0" class="font-italic">Nimaš oddanih predlogov.</p>
            <b-row>
              <b-col
                v-if="published.length === 0"
                cols="12"
                lg="6"
                xl="4"
                class="mb-4"
              >
                <div class="initiative-card py-5 px-3 empty h-100 text-center">
                  <h4>Oddaj predlog izboljšave, popravek ali postavi vprašanje</h4>
                  <div>
                    <NuxtLink
                      to="/predlogi/nov"
                      class="new-initiative-button btn position-relative d-inline-flex justify-content-center text-uppercase"
                    >
                      Predlagaj
                      <img src="~/assets/img/icons/arrow-right.png" alt="logout icon" class="position-absolute">
                    </NuxtLink>
                  </div>
                </div>
              </b-col>
              <b-col
                v-for="initiative in published"
                :key="initiative.id"
                cols="12"
                lg="6"
                xl="4"
                class="mb-4"
              >
                <InitiativeCard
                  v-bind="initiative"
                  @vote="vote(initiative.id)"
                >
                </InitiativeCard>
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
  asyncData ({ store }) {
    return store.dispatch('getMyInitiatives')
  },
  data () {
    return {
      drafts: [],
      published: []
    }
  },
  methods: {
    async logout () {
      await this.$store.dispatch('logout')
    },
    async vote (id) {
      const success = await this.$store.dispatch('postVote', {
        id
      })
      if (success) { // voted successfully
        for (const initiative of this.published) {
          if (initiative.id === id) {
            initiative.has_voted = true
            initiative.vote_count += 1
            break
          }
        }
      } else { // error
        console.log('error')
      }
    },
    date (date) {
      const d = new Date(date)
      return `${d.getDate()}.${d.getMonth() + 1}.${d.getFullYear()}`
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

  &.empty {
    h4 {
      font-weight: 600;
    }

    .new-initiative-button {
      padding-right: 2.5rem;
      padding-left: 1rem;

      &:hover {
        background-color: #6c757d;
        color: white;
      }

      img {
        right: 0.5rem;
        height: 1.5rem;
      }
    }
  }
}

</style>
