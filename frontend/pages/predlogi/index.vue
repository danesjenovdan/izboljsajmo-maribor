<template>
  <b-container fluid class="h-100">
    <b-row class="h-100">
      <b-col lg="7">
        <b-row class="my-4 justify-content-center">
          <b-col cols="9" class="text-center">
            <h4 class="d-inline">
              Oddaj pobudo!
            </h4> Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.
          </b-col>
        </b-row>
        <b-row class="action-cards">
          <b-col cols="4">
            <div class="action-card-top" />
            <NuxtLink to="/predlogi/nov" class="action-card d-block h-100">
              <h6 class="d-flex align-items-center">
                MOTI ME!
                <img src="~/assets/img/icons/arrow-right.png" alt="arrow right">
              </h6>
              <p>Naznani okvare, poškodbe, slabosti (pomanjkljivosti), ki jih zaznavaš v svojem okolju.</p>
            </NuxtLink>
          </b-col>
          <b-col cols="4">
            <div class="action-card-top" />
            <div class="action-card h-100">
              <h6 class="d-flex align-items-center">
                IMAM IDEJO!
                <img src="~/assets/img/icons/arrow-right.png" alt="arrow right">
              </h6>
              <p>Predlagaj novosti,  predloge za izboljšave, družbene inovacije, ki izboljšujejo kakovost življenja v MO Maribor.</p>
            </div>
          </b-col>
          <b-col cols="4">
            <div class="action-card-top" />
            <div class="action-card h-100">
              <h6 class="d-flex align-items-center">
                ZANIMA ME!
                <img src="~/assets/img/icons/arrow-right.png" alt="arrow right">
              </h6>
              <p>Zastavi splošna vprašanja ali izreči pohvale.</p>
            </div>
          </b-col>
        </b-row>
        <hr class="hr-upper">
        <hr class="hr-lower">
        <div>
          <b-row>
            <b-col cols="12">
              <h4 class="mb-4 text-center">
                Išči ali brskaj po obstoječih predlogih!
              </h4>
            </b-col>
          </b-row>
          <b-row class="mb-4">
            <b-col cols="12" class="d-flex">
              <div class="d-inline-flex flex-grow-1 align-items-center position-relative">
                <input
                  v-model="search"
                  type="text"
                  class="form-control"
                  placeholder="Išči po naslovu ali vsebini pobud"
                >
                <img src="~/assets/img/icons/search.png" class="position-absolute mr-1" style="right: 0;">
              </div>
              <button
                class="filter d-inline-flex align-items-center"
                @click="showType = !showType"
              >
                Tip
                <img
                  src="~/assets/img/icons/arrow-down.png"
                  alt="arrow down"
                  :class="{ 'ml-2': true, 'dropdown-open': showType }"
                >
                <div
                  v-if="showType"
                  style="position: absolute; top: 3rem; z-index: 1"
                  @click.stop=""
                >
                  <div>
                    TO DO: types
                  </div>
                </div>
              </button>
              <button
                class="filter d-inline-flex align-items-center"
                @click="showArea = !showArea"
              >
                Področje
                <img
                  src="~/assets/img/icons/arrow-down.png"
                  alt="arrow down"
                  :class="{ 'ml-2': true, 'dropdown-open': showArea }"
                >
                <div
                  v-if="showArea"
                  style="position: absolute; top: 3rem; z-index: 1"
                  @click.stop=""
                >
                  <div>
                    TO DO: areas
                  </div>
                </div>
              </button>
              <button
                class="filter d-inline-flex align-items-center"
                @click="showLocation = !showLocation"
              >
                Območje
                <img
                  src="~/assets/img/icons/arrow-down.png"
                  alt="arrow down"
                  :class="{ 'ml-2': true, 'dropdown-open': showLocation }"
                >
                <div
                  v-if="showLocation"
                  style="position: absolute; top: 3rem; z-index: 1"
                  @click.stop=""
                >
                  <div>
                    TO DO: območje
                  </div>
                </div>
              </button>
              <button
                class="filter d-inline-flex align-items-center"
                @click="showStatus = !showStatus"
              >
                Status
                <img
                  src="~/assets/img/icons/arrow-down.png"
                  alt="arrow down"
                  :class="{ 'ml-2': true, 'dropdown-open': showStatus }"
                >
                <div
                  v-if="showStatus"
                  style="position: absolute; top: 3rem; z-index: 1"
                  @click.stop=""
                >
                  <div>
                    TO DO: status
                  </div>
                </div>
              </button>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col class="d-flex justify-content-between">
              <div>
                {{ initiatives.length }} predlogov
              </div>
              <div>
                Sortiraj po datumu objave
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col v-for="initiative in initiatives" :key="initiative.id" cols="4" class="mb-4">
              <div class="initiative-card h-100">
                <img
                  v-if="initiative.cover_image"
                  class="cover-image"
                  :src="initiative.cover_image.image"
                  alt=""
                >
                <div class="initiative-card-body">
                  <h4>
                    <NuxtLink :to="`/predlogi/${initiative.id}`">
                      {{ initiative.title }}
                    </NuxtLink>
                  </h4>
                  <span class="author">{{ initiative.author }}</span>
                  <div class="my-1">
                    <span class="tag">{{ initiative.status }}</span>
                    <span class="tag">{{ initiative.area.name }}</span>
                    <span class="tag">{{ date(initiative.created) }}</span>
                  </div>
                  <p>
                    {{ initiative.description }}
                  </p>
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
        </div>
      </b-col>
      <b-col lg="5">
        <div id="map-wrap" class="h-100">
          <client-only>
            <l-map :zoom=13 :center="[46.554650,15.645881]">
              <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></l-tile-layer>
              <l-marker
                v-for="initiative in initiatives"
                :key="initiative.id"
                :lat-lng="[initiative.location.coordinates[0],initiative.location.coordinates[1]]"
              >
              </l-marker>
            </l-map>
          </client-only>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  components: {
  },
  data () {
    return {
      search: '',
      showType: false,
      showArea: false,
      showLocation: false,
      showStatus: false,
      initiatives: [],
      map: null
    }
  },
  computed: {
  },
  created () {
    this.fetchInitiatives()
  },
  methods: {
    async fetchInitiatives () {
      const response = await this.$axios.get('v1/initiatives/')
      const responseData = await response.data
      if (response.status === 200) {
        console.log(responseData)
        for (const i in responseData) {
          this.initiatives.push(responseData[i])
          console.log(this.initiatives[i].location.coordinates)
        }
      } else {
        console.log('ni ok', responseData)
        // throw error
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

.action-card {
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;
  border-radius: 0.5rem;
  padding: 1rem 1rem 1rem 1.5rem;
  cursor: pointer;
  color: black;
  text-decoration: none;

  &:hover {
    background-color: #eff3fb;
  }

  h6 {
    font-weight: 700;
    font-style: italic;
    text-transform: uppercase;
    letter-spacing: 0.1rem;

    img {
      height: 1.2rem;
      margin-left: 0.5rem;
    }
  }

  p {
    font-size: 0.8rem;
    font-style: italic;
  }
}

.action-cards {
  div:nth-child(1) .action-card-top {
    background-color: #8cade2;
  }
  div:nth-child(2) .action-card-top {
    background-color: #70b6a3;
  }
  div:nth-child(3) .action-card-top {
    background-color: #d9ab27;
  }
}

.action-card-top {
  height: 100%;
  width: 0.5rem;
  position: absolute;
  border-top-left-radius: 0.5rem;
  border-bottom-left-radius: 0.5rem;
}

h4 {
  font-weight: 600;
}

.filter {
  box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
  border-radius: 1.5rem;
  border: none;
  font-style: italic;
  font-size: 0.8rem;
  padding: 0.1rem 0.5rem;
  margin-left: 0.5rem;

  img {
    transition: transform 500ms;

    &.dropdown-open {
      transform: rotate(-180deg);
    }
  }
}

.initiative-card {
  box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;

  .cover-image {
    width: 100%;
    height: 8rem;
    object-fit: cover;
  }

  .initiative-card-body {
    padding: 0.5rem;

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
