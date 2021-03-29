<template>
  <b-container fluid>
    <b-row class="p-4">
      <b-col cols="12" lg="3" class="text-center text-lg-left mb-4">
        <h1>Pozdravljeni, {{ this.$auth.user.username }}!</h1>
        <b-button
          class="logout-button w-75 position-relative d-inline-flex justify-content-center align-items-center"
          @click="logout"
        >
          ODJAVA
          <ExitRightIcon class="position-absolute" />
        </b-button>
      </b-col>
      <b-col cols="12" lg="9">
        <b-row v-if="drafts.length > 0" class="card-outline p-4 mb-4">
          <b-col cols="12" md="4" lg="2" class="mb-4">
            <h4>Neoddane pobude</h4>
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
                <NuxtLink :to="`/predlogi/oddaj/${editLink[draft.type]}?id=${draft.id}`">
                  <div class="initiative-card draft h-100">
                    <img
                      v-if="draft.cover_image"
                      class="cover-image"
                      :src="draft.cover_image.image"
                      alt="Initiative draft cover image"
                    >
                    <div class="initiative-card-body">
                      <h4>{{ draft.title }}</h4>
                      <p>{{ draft.description }}</p>
                      <div class="d-flex justify-content-center">
                        <div class="d-inline-flex align-items-center">
                          <NuxtLink
                            :to="`/predlogi/oddaj/${editLink[draft.type]}?id=${draft.id}`"
                            class="btn d-flex align-items-center position-relative"
                          >
                            <span class="text-uppercase pr-2">Uredi</span>
                            <EditIcon class="position-absolute" />
                          </NuxtLink>
                        </div>
                      </div>
                    </div>
                  </div>
                </NuxtLink>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <b-row class="card-outline p-4 mb-4">
          <b-col cols="12" md="4" lg="2" class="mb-4">
            <h4>Oddane pobude</h4>
          </b-col>
          <b-col cols="12" md="8" lg="10">
            <p v-if="published.length === 0" class="font-italic">
              Nimate oddanih pobud.
            </p>
            <b-row>
              <b-col
                v-if="published.length === 0"
                cols="12"
                lg="6"
                xl="4"
                class="mb-4"
              >
                <div class="initiative-card py-5 px-3 empty h-100 text-center">
                  <h4>Oddajte predlog izboljšave, popravek ali postavite vprašanje</h4>
                  <div>
                    <NuxtLink
                      to="/predlogi/nov?tip=II"
                      class="new-initiative-button btn position-relative d-inline-flex justify-content-center text-uppercase"
                    >
                      Predlagaj
                      <img src="~/assets/img/icons/arrow-right.svg" alt="logout icon" class="position-absolute">
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
                  @removeVote="removeVote(initiative.id)"
                />
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import InitiativeCard from '~/components/InitiativeCard'
import ExitRightIcon from '~/assets/img/icons/exit-right.svg?inline'
import EditIcon from '~/assets/img/icons/edit.svg?inline'

export default {
  components: { InitiativeCard, ExitRightIcon, EditIcon },
  middleware: 'auth',
  asyncData ({ store }) {
    return store.dispatch('getMyInitiatives')
  },
  data () {
    return {
      drafts: [],
      published: [],
      editLink: {
        MM: 'moti-me',
        ZM: 'zanima-me',
        II: 'imam-idejo'
      }
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
        this.updateVotes(id, true)
      } else { // error
        console.log('error')
      }
    },
    async removeVote (id) {
      const success = await this.$store.dispatch('deleteVote', {
        id
      })
      if (success) { // unvoted successfully
        this.updateVotes(id, false)
      } else { // error
        console.log('error')
      }
    },
    updateVotes (id, hasVoted) {
      for (const initiative of this.published) {
        if (initiative.id === id) {
          initiative.has_voted = hasVoted
          initiative.vote_count += hasVoted ? 1 : -1
          break
        }
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
    background-color: #1A365D;
  }
}

.card-outline {
  box-shadow: 4px 4px 11px #d4d9e1, -5px -5px 11px #ffffff;
  border-radius: 0.5rem;
}

a {
  color: unset;

  &:hover {
    text-decoration: none;
  }
}

.initiative-card {
  box-shadow: 4px 4px 6px #d3d7df, -4px -4px 6px #ffffff;

  &:hover {
    background-color: white;
  }

  .cover-image {
    width: 100%;
    height: 8rem;
    object-fit: cover;
  }

  .initiative-card-body {
    padding: 0.75rem;

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

  &.draft {
    .btn {
      padding: 0.75rem 3rem;
      font-size: 1rem;
      font-style: italic;
      font-weight: 700;
      letter-spacing: 2px;

      svg {
        height: 1.5rem;
        width: 1.5rem;
        right: 1rem;
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
