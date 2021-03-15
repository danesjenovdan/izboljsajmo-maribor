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
                <button class="search-button position-absolute" @click="fetchInitiatives">
                  <img src="~/assets/img/icons/search.png">
                </button>
              </div>
              <button
                class="filter d-inline-flex align-items-center"
                :class="{ 'dropdown-open': showType }"
                @click="switchType"
              >
                Tip
                <img
                  src="~/assets/img/icons/arrow-down.png"
                  alt="arrow down"
                  class="ml-2"
                >
                <div
                  v-if="showType"
                  class="filter-dropdown position-absolute"
                  @click.stop=""
                >
                  <div>
                    <b-form-group>
                      <b-form-checkbox
                        id="filter-type-MM"
                        v-model="filterTypes"
                        value="MM"
                        @change="fetchInitiatives"
                      >
                        MOTI ME!
                      </b-form-checkbox>
                      <b-form-checkbox
                        id="filter-type-II"
                        v-model="filterTypes"
                        value="II"
                        @change="fetchInitiatives"
                      >
                        IMAM IDEJO!
                      </b-form-checkbox>
                      <b-form-checkbox
                        id="filter-type-ZM"
                        v-model="filterTypes"
                        value="ZM"
                        @change="fetchInitiatives"
                      >
                        ZANIMA ME!
                      </b-form-checkbox>
                    </b-form-group>
                  </div>
                </div>
              </button>
              <button
                class="filter d-inline-flex align-items-center"
                :class="{ 'dropdown-open': showArea }"
                @click="switchArea"
              >
                Področje
                <img
                  src="~/assets/img/icons/arrow-down.png"
                  alt="arrow down"
                  class="ml-2"
                >
                <div
                  v-if="showArea"
                  class="filter-dropdown position-absolute"
                  @click.stop=""
                >
                  <div>
                    <b-form-group>
                      <b-form-checkbox
                        v-for="area in this.areas"
                        :id="String(area.id)"
                        :key="area.id"
                        v-model="filterAreas"
                        :value="area.id"
                        @change="fetchInitiatives"
                      >
                        <div>{{ area.name }}</div>
                        <div>{{ area.note }}</div>
                      </b-form-checkbox>
                    </b-form-group>
                  </div>
                </div>
              </button>
              <button
                class="filter d-inline-flex align-items-center"
                :class="{ 'dropdown-open': showZone }"
                @click="switchZone"
              >
                Območje
                <img
                  src="~/assets/img/icons/arrow-down.png"
                  alt="arrow down"
                  class="ml-2"
                >
                <div
                  v-if="showZone"
                  class="filter-dropdown position-absolute"
                  @click.stop=""
                >
                  <div>
                    <b-form-group>
                      <b-form-checkbox
                        v-for="zone in this.zones"
                        :id="String(zone.id)"
                        :key="zone.id"
                        v-model="filterZones"
                        :value="zone.id"
                        @change="fetchInitiatives"
                      >
                        {{ zone.name }}
                      </b-form-checkbox>
                    </b-form-group>
                  </div>
                </div>
              </button>
              <button
                class="filter d-inline-flex align-items-center"
                :class="{ 'dropdown-open': showStatus }"
                @click="switchStatus"
              >
                Status
                <img
                  src="~/assets/img/icons/arrow-down.png"
                  alt="arrow down"
                  class="ml-2"
                >
                <div
                  v-if="showStatus"
                  class="filter-dropdown position-absolute"
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
              <div
                class="sort-initiatives d-flex align-items-center"
                @click="sortInitiativesByDateAscending = !sortInitiativesByDateAscending"
              >
                <span>Sortiraj po datumu objave</span>
                <img
                  src="~/assets/img/icons/down-arrow.png"
                  alt="down-arrow"
                  class="ml-1"
                  :class="{ 'sort-ascending': sortInitiativesByDateAscending }"
                >
              </div>
            </b-col>
          </b-row>
          <b-row>
            <InitiativeCard
              v-for="initiative in sortedInitiatives"
              :key="initiative.id"
              v-bind="initiative"
              @vote="vote(initiative.id)"
            >
            </InitiativeCard>
          </b-row>
        </div>
      </b-col>
      <b-col lg="5">
        <div id="map-wrap" class="h-100">
          <client-only>
            <l-map
              :zoom="15"
              :center="[46.554650, 15.645881]"
            >
              <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png" />
              <l-marker
                v-for="initiative in initiatives"
                :key="initiative.id"
                :lat-lng="[initiative.location.coordinates[0], initiative.location.coordinates[1]]"
                :icon="mapIcon"
                @ready="setIconStyles"
              />
            </l-map>
          </client-only>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import InitiativeCard from '~/components/InitiativeCard'

export default {
  components: { InitiativeCard },
  asyncData ({ store }) {
    return store.dispatch('getInitiatives', {})
  },
  data () {
    return {
      search: '',
      showType: false,
      filterTypes: [],
      areas: [],
      showArea: false,
      filterAreas: [],
      zones: [],
      showZone: false,
      filterZones: [],
      showStatus: false,
      filterStatuses: [],
      sortInitiativesByDateAscending: true,
      initiatives: [],
      map: null,
      mapIcon: null
    }
  },
  computed: {
    sortedInitiatives () {
      const initiatives = this.initiatives.slice(0).sort((a, b) => a.created.localeCompare(b.created))
      if (!this.sortInitiativesByDateAscending) {
        initiatives.reverse()
      }
      return initiatives
    }
  },
  created () {
    this.fetchAreas()
    this.fetchZones()
  },
  methods: {
    setIconStyles () {
      this.mapIcon = this.$L.icon({
        iconUrl: require('@/assets/img/icons/pin.png')
      })
    },
    async fetchInitiatives () {
      const fetched = await this.$store.dispatch('getInitiatives', {
        search: this.search,
        type: this.filterTypes,
        area: this.filterAreas,
        zone: this.filterZones,
        status: this.filterStatuses
      })
      this.initiatives = fetched.initiatives
    },
    async fetchAreas () {
      this.areas = await this.$store.dispatch('getAreas')
    },
    async fetchZones () {
      this.zones = await this.$store.dispatch('getZones')
    },
    switchType () {
      this.showType = !this.showType
      this.showArea = false
      this.showZone = false
      this.showStatus = false
    },
    switchArea () {
      this.showType = false
      this.showArea = !this.showArea
      this.showZone = false
      this.showStatus = false
    },
    switchZone () {
      this.showType = false
      this.showArea = false
      this.showZone = !this.showZone
      this.showStatus = false
    },
    switchStatus () {
      this.showType = false
      this.showArea = false
      this.showZone = false
      this.showStatus = !this.showStatus
    },
    async vote (id) {
      const success = await this.$store.dispatch('postVote', {
        id
      })
      if (success) { // voted successfully
        for (const initiative of this.initiatives) {
          if (initiative.id === id) {
            initiative.has_voted = true
            initiative.vote_count += 1
            break
          }
        }
      } else { // error
        console.log('error')
      }
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

.search-button {
  border: none;
  background-color: transparent;
  right: 0;

  img {
    height: 2rem;
  }
}

.filter {
  box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
  border-radius: 1.5rem;
  border: 1px solid #f8f8f8;
  font-style: italic;
  font-size: 0.8rem;
  padding: 0.1rem 0.5rem;
  margin-left: 0.5rem;

  &.dropdown-open {
    border: 1px solid #ef7782;

    img {
      transform: rotate(-180deg);
    }
  }

  img {
    transition: transform 500ms;
  }

  .filter-dropdown {
    background-color: #f8f8f8;
    box-shadow: 0 0 2rem rgba(0, 0, 0, 0.2);
    border-radius: 0.5rem;
    top: 3rem;
    z-index: 10;
    padding: 1rem;
    text-align: left;
  }
}

.sort-initiatives {
  font-size: 0.8rem;
  box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
  background-color: #e8ebef;
  border-radius: 0.75rem;
  padding: 0.25rem 0.75rem;
  cursor: pointer;

  &:hover {
    background-color: #5a6268;
    color: white;
  }

  img {
    height: 0.8rem;
    transition: transform 500ms;

    &.sort-ascending {
      transform: rotate(180deg);
    }
  }
}

</style>
