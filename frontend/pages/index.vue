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
                cols="12"
                class="masonry"
              >
                <div
                  v-for="(draft, index) in drafts"
                  :key="`draft-${index}`"
                  class="masonry-item"
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
                </div>
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
                    <button
                      class="new-initiative-dropdown-btn d-inline-flex align-items-center position-relative ml-0 mt-3"
                      :class="{ 'dropdown-open': newInitiativeDropdown }"
                      @click="openNewInitiativeDropdown"
                    >
                      Kakšno pobudo želite oddati?
                      <ArrowDownIcon class="ml-2" />
                      <div
                        v-if="newInitiativeDropdown"
                        class="new-initiative-dropdown position-absolute"
                        @click.stop=""
                      >
                        <div class="form-note">Izberite tip pobude.</div>
                        <hr class="hr-upper mt-0">
                        <hr class="hr-lower mb-0">
                        <div>
                          <b-form-group>
                            <b-form-radio v-model="newInitiativeType" value="MM" class="p-0 pl-4">
                              <h5 class="font-weight-bold">
                                MOTI ME!
                              </h5>
                              <p class="form-note">
                                Naznani okvare, poškodbe, slabosti (pomanjkljivosti), ki jih zaznavaš v svojem okolju.
                              </p>
                            </b-form-radio>
                            <b-form-radio v-model="newInitiativeType" value="II" class="p-0 pl-4">
                              <h5 class="font-weight-bold">
                                IMAM IDEJO!
                              </h5>
                              <p class="form-note">
                                Predlagaj novosti,  predloge za izboljšave, družbene inovacije, ki izboljšujejo kakovost življenja v MO Maribor.
                              </p>
                            </b-form-radio>
                            <b-form-radio v-model="newInitiativeType" value="ZM" class="p-0 pl-4">
                              <h5 class="font-weight-bold">
                                ZANIMA ME!
                              </h5>
                              <p class="form-note">
                                Zastavi splošna vprašanja ali izreči pohvale.
                              </p>
                            </b-form-radio>
                          </b-form-group>
                          <div class="p-0 my-3 w-100 d-flex justify-content-center">
                            <NuxtLink
                              :to="`/predlogi/oddaj/${editLink[newInitiativeType]}`"
                              class="new-initiative-button btn d-inline-flex justify-content-center align-items-center text-uppercase"
                            >
                              Predlagaj
                              <ArrowRightIcon class="ml-2" />
                            </NuxtLink>
                          </div>
                        </div>
                      </div>
                    </button>
                  </div>
                </div>
              </b-col>
              <b-col>
                <div class="masonry">
                  <div
                    v-for="initiative in published"
                    :key="`published-${initiative.id}`"
                    class="masonry-item"
                  >
                    <InitiativeCard
                      v-bind="initiative"
                      @vote="vote(initiative.id)"
                      @removeVote="removeVote(initiative.id)"
                    />
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
import InitiativeCard from '~/components/InitiativeCard'
import ExitRightIcon from '~/assets/img/icons/exit-right.svg?inline'
import EditIcon from '~/assets/img/icons/edit.svg?inline'
import ArrowDownIcon from '~/assets/img/icons/arrow-down.svg?inline'
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'

export default {
  components: { InitiativeCard, ExitRightIcon, EditIcon, ArrowDownIcon, ArrowRightIcon },
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
      },
      newInitiativeDropdown: false,
      newInitiativeType: '',
      columns: 1
    }
  },
  mounted () {
    if (window.matchMedia('(min-width: 1800px)').matches) {
      this.columns = 4
    } else if (window.matchMedia('(min-width: 1200px)').matches) {
      this.columns = 3
    } else if (window.matchMedia('(min-width: 576px)').matches) {
      this.columns = 2
    } else {
      this.columns = 1
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
    },
    openNewInitiativeDropdown () {
      this.newInitiativeDropdown = !this.newInitiativeDropdown
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
    &:hover {
      background-color: white;
    }

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
      padding: 0.5rem 1rem;
      font-size: 1.25rem;
      letter-spacing: 2px;

      &:hover {
        background-color: #1A365D;
        color: white;
      }

      svg {
        right: 0.5rem;
        height: 1.5rem;
        width: 1.5rem;
      }
    }
  }
}

.new-initiative-dropdown-btn {
  box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
  border-radius: 1.5rem;
  border: 2px solid #f8f8f8;
  background-color: #f8f8f8;
  font-style: italic;
  padding: 0.25rem 1rem;

  &:hover {
    background-color: white;
    border-color: white;
  }

  &.dropdown-open {
    border: 2px solid #ef7782;

    &:hover {
      border-color: #ef7782;
    }
  }

  & > svg {
    max-width: 0.5rem;
    max-height: 0.5rem;
  }

  .new-initiative-dropdown {
    background-color: #f8f8f8;
    box-shadow: 0 0 2rem rgba(0, 0, 0, 0.2);
    border-radius: 0.5rem;
    top: 6rem;
    z-index: 10;
    text-align: left;
    cursor: default;

    h5 {
      letter-spacing: 2px;
    }

    div.form-note {
      padding: 1rem 2rem;
    }

    .form-note {
      font-size: 0.8rem;
      font-weight: 400;
      margin-bottom: 0;
    }

    div {
      padding-left: 1.5rem;
      padding-right: 1rem;
    }

    @media (min-width: 768px) {
      top: 3rem;
    }

    @media (min-width: 992px) {
      left: auto;
      right: auto;
    }
  }
}

</style>
