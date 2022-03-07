<template>
  <b-container fluid class="h-100">
    <b-row class="h-100">
      <b-col lg="7" class="h-100 overflow-auto">
        <b-row class="my-4 justify-content-center">
          <b-col cols="12" lg="9" class="text-center landing-title">
            <h4 class="mb-0">
              Dobrodošli na platformi Izboljšajmo Maribor!
            </h4>
            <p>
              Kliknite na enega od spodnjih gumbov in nam posredujte svojo pobudo.
            </p>
          </b-col>
        </b-row>
        <b-row class="action-cards">
          <b-col cols="12" md="4" class="mb-3">
            <div class="action-card-top" />
            <NuxtLink to="/predlogi/oddaj/zanima-me" class="action-card d-block h-100">
              <h6 class="d-flex align-items-center">
                ZANIMA ME
                <ArrowRightIcon />
              </h6>
              <p>Splošna vprašanja / pohvale</p>
            </NuxtLink>
          </b-col>
          <b-col cols="12" md="4" class="mb-3">
            <div class="action-card-top" />
            <NuxtLink to="/predlogi/oddaj/moti-me" class="action-card d-block h-100">
              <h6 class="d-flex align-items-center">
                MOTI ME
                <ArrowRightIcon />
              </h6>
              <p>Zaznane okvare, poškodbe, slabosti, pomanjkljivosti, nepravilnosti ...</p>
            </NuxtLink>
          </b-col>
          <b-col cols="12" md="4" class="mb-3">
            <div class="action-card-top" />
            <NuxtLink to="/predlogi/oddaj/imam-idejo" class="action-card d-block h-100">
              <h6 class="d-flex align-items-center">
                IMAM IDEJO
                <ArrowRightIcon />
              </h6>
              <p>Projektni predlogi, novosti, predlogi za izboljšave, družbene inovacije ...</p>
            </NuxtLink>
          </b-col>
        </b-row>
        <hr class="hr-upper">
        <hr class="hr-lower">
        <div>
          <b-row>
            <b-col cols="12">
              <h4 class="mb-4 text-center">
                Iščite ali brskajte po že oddanih pobudah
              </h4>
            </b-col>
          </b-row>
          <b-row class="mb-4">
            <b-col cols="12" class="d-md-flex">
              <div class="d-flex d-md-inline-flex flex-grow-1 mb-3 mb-md-0 mr-0 mr-md-2 align-items-center">
                <div class="w-100 position-relative">
                  <input
                    v-model="search"
                    type="text"
                    class="form-control"
                    placeholder="Iščite po naslovu ali vsebini pobud"
                    @keyup.enter="fetchInitiatives"
                  >
                  <button class="search-button position-absolute" @click="fetchInitiatives">
                    <SearchIcon />
                  </button>
                </div>
              </div>
              <div class="d-flex d-md-inline-flex justify-content-end">
                <button
                  id="type-filter-button"
                  class="filter d-inline-flex align-items-center ml-0"
                  :class="{ 'dropdown-open': showType }"
                  @click="switchType"
                >
                  Tip
                  <ArrowDownIcon class="ml-2" />
                  <div
                    v-if="showType"
                    v-click-outside="closeTypeDropdown"
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
                  id="area-filter-button"
                  class="filter d-inline-flex align-items-center"
                  :class="{ 'dropdown-open': showArea }"
                  @click="switchArea"
                >
                  Področje
                  <ArrowDownIcon class="ml-2" />
                  <div
                    v-if="showArea"
                    v-click-outside="closeAreaDropdown"
                    class="filter-dropdown position-absolute"
                    @click.stop=""
                  >
                    <div>
                      <b-form-group>
                        <b-form-checkbox
                          v-for="area in areas"
                          :id="String(area.id)"
                          :key="area.id"
                          v-model="filterAreas"
                          :value="area.id"
                          @change="fetchInitiatives"
                        >
                          <div>{{ area.name }}</div>
                          <!-- <div>{{ area.note }}</div> -->
                        </b-form-checkbox>
                      </b-form-group>
                    </div>
                  </div>
                </button>
                <button
                  id="zone-filter-button"
                  class="filter d-inline-flex align-items-center"
                  :class="{ 'dropdown-open': showZone }"
                  @click="switchZone"
                >
                  Območje
                  <ArrowDownIcon class="ml-2" />
                  <div
                    v-if="showZone"
                    v-click-outside="closeZoneDropdown"
                    class="filter-dropdown position-absolute"
                    @click.stop=""
                  >
                    <div>
                      <b-form-group>
                        <b-form-checkbox
                          v-for="zone in zones"
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
                  id="status-filter-button"
                  class="filter d-inline-flex align-items-center"
                  :class="{ 'dropdown-open': showStatus }"
                  @click="switchStatus"
                >
                  Status
                  <ArrowDownIcon class="ml-2" />
                  <div
                    v-if="showStatus"
                    v-click-outside="closeStatusDropdown"
                    class="filter-dropdown position-absolute"
                    style="right: 0.5rem;"
                    @click.stop=""
                  >
                    <div>
                      <b-form-group>
                        <b-form-checkbox
                          v-for="status in statuses"
                          :id="String(status.id)"
                          :key="status.id"
                          v-model="filterStatuses"
                          :value="status.id"
                          @change="fetchInitiatives"
                        >
                          {{ status.name }}
                        </b-form-checkbox>
                      </b-form-group>
                    </div>
                  </div>
                </button>
              </div>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col class="d-flex justify-content-between">
              <div class="initiatives-no pl-1 d-flex align-items-center">
                {{ initiativesNumber }}
              </div>
              <div
                class="sort-initiatives d-flex align-items-center"
                @click="sortInitiativesByDateAscending = !sortInitiativesByDateAscending; sortInitiatives()"
              >
                <span class="mr-1">Sortiraj po datumu objave</span>
                <DownArrowIcon class="ml-1" :class="{ 'sort-ascending': sortInitiativesByDateAscending }" />
              </div>
            </b-col>
          </b-row>
          <client-only>
            <div
              v-if="sortedInitiatives.length > 0"
              class="p-4 p-md-0"
            >
              <div id="masonry" v-masonry="'masonry'" item-selector=".item" class="masonry-container">
                <div
                  v-for="initiative in sortedInitiatives"
                  :key="initiative.id"
                  v-masonry-tile
                  horizontal-order="true"
                  class="item px-2 pb-3"
                >
                  <InitiativeCard
                    v-bind="initiative"
                    @vote="vote(initiative.id)"
                    @removeVote="removeVote(initiative.id)"
                  />
                </div>
              </div>
            </div>
          </client-only>
          <b-row v-if="sortedInitiatives.length === 0">
            <b-col cols="12" class="d-inline-flex justify-content-center mb-5">
              <div class="d-flex justify-content-center align-items-center mt-4 no-initiatives">
                <FolderEmptyIcon />
                <span class="ml-2">Za izbrane filtre ni oddane nobene pobude.</span>
              </div>
            </b-col>
          </b-row>
        </div>
      </b-col>
      <b-col lg="5" class="px-0">
        <div id="map-wrap" class="h-100">
          <client-only>
            <l-map
              :zoom="14"
              :min-zoom="11"
              :center="[46.554650, 15.645881]"
              :max-bounds="[
                [46.46188844675249, 15.51583465730236],
                [46.62102957408261, 15.783283325506178]
              ]"
            >
              <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png" />
              <l-marker
                v-for="initiative in initiativeMarkers"
                :key="initiative.id"
                :lat-lng="[initiative.location.coordinates[1], initiative.location.coordinates[0]]"
                :icon="mapIcon"
                @ready="setIconStyles"
                @click="markerClick(initiative.id)"
              />
            </l-map>
          </client-only>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'
import ArrowDownIcon from '~/assets/img/icons/arrow-down.svg?inline'
import DownArrowIcon from '~/assets/img/icons/down-arrow.svg?inline'
import FolderEmptyIcon from '~/assets/img/icons/folder-question-mark.svg?inline'
import SearchIcon from '~/assets/img/icons/search.svg?inline'
import InitiativeCard from '~/components/InitiativeCard'

export default {
  components: { ArrowRightIcon, ArrowDownIcon, DownArrowIcon, FolderEmptyIcon, SearchIcon, InitiativeCard },
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
      statuses: [],
      showStatus: false,
      filterStatuses: [],
      sortInitiativesByDateAscending: false,
      initiatives: [],
      sortedInitiatives: [],
      map: null,
      mapIcon: null,
      columns: 1
    }
  },
  computed: {
    initiativesNumber () {
      const n = this.initiatives.length
      if (n === 1) { return '1 predlog' } else if (n === 2) { return '2 predloga' } else if (n === 3 || n === 4) { return `${n} predlogi` } else { return `${n} predlogov` }
    },
    initiativeMarkers () {
      return this.initiatives.filter(initiative => initiative.location)
    }
  },
  async created () {
    await this.fetchAreas()
    await this.fetchZones()
    await this.fetchStatuses()
    await this.fetchInitiatives()
  },
  methods: {
    setIconStyles () {
      this.mapIcon = this.$L.icon({
        iconUrl: require('@/assets/img/icons/pin.svg'),
        iconSize: [32, 32]
      })
    },
    markerClick (id) {
      const offset = 47 // sticky nav height
      const container = document.getElementById('masonry')
      const el = document.getElementById(`initiative-card-${id}`).parentElement // element you are scrolling to
      window.scroll({ top: (el.offsetTop + container.offsetTop - offset), left: 0, behavior: 'smooth' })
      document.getElementById(`initiative-card-${id}`).style.outlineColor = '#1a365d'
      setTimeout(function () {
        document.getElementById(`initiative-card-${id}`).style.outlineColor = 'transparent'
      }, 1000)
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
      this.sortInitiatives()
    },
    sortInitiatives () {
      const sortedByTime = this.initiatives.slice(0).sort((a, b) => a.created.localeCompare(b.created))
      if (!this.sortInitiativesByDateAscending) {
        sortedByTime.reverse()
      }
      this.sortedInitiatives = sortedByTime
      this.$nextTick(() => this.$redrawVueMasonry('masonry'))
    },
    async fetchAreas () {
      this.areas = await this.$store.dispatch('getAreas')
      // this.filterAreas = this.areas.map(a => a.id)
    },
    async fetchZones () {
      this.zones = await this.$store.dispatch('getZones')
      // this.filterZones = this.zones.map(z => z.id)
    },
    async fetchStatuses () {
      const statuses = await this.$store.dispatch('getStatuses')
      if (statuses) {
        const filteredStatuses = statuses.filter(st => {
          return st.name !== "Zavrnjeno"
        })
        this.statuses = filteredStatuses.sort((a, b) => parseInt(a['id']) > parseInt(b['id']))
      }
    },
    switchType () {
      this.showType = !this.showType
      this.showArea = false
      this.showZone = false
      this.showStatus = false
    },
    closeTypeDropdown (e) {
      if (e.target.id !== 'type-filter-button') {
        this.showType = false
      }
    },
    switchArea () {
      this.showType = false
      this.showArea = !this.showArea
      this.showZone = false
      this.showStatus = false
    },
    closeAreaDropdown (e) {
      if (e.target.id !== 'area-filter-button') {
        this.showArea = false
      }
    },
    switchZone () {
      this.showType = false
      this.showArea = false
      this.showZone = !this.showZone
      this.showStatus = false
    },
    closeZoneDropdown (e) {
      if (e.target.id !== 'zone-filter-button') {
        this.showZone = false
      }
    },
    switchStatus () {
      this.showType = false
      this.showArea = false
      this.showZone = false
      this.showStatus = !this.showStatus
    },
    closeStatusDropdown (e) {
      if (e.target.id !== 'status-filter-button') {
        this.showStatus = false
      }
    },
    async vote (id) {
      const success = await this.$store.dispatch('postVote', {
        id
      })
      if (success) { // voted successfully
        this.updateVotes(id, true)
      } else { // error
        // console.log('error')
      }
    },
    async removeVote (id) {
      const success = await this.$store.dispatch('deleteVote', {
        id
      })
      if (success) { // unvoted successfully
        this.updateVotes(id, false)
      } else { // error
        // console.log('error')
      }
    },
    updateVotes (id, hasVoted) {
      for (const initiative of this.initiatives) {
        if (initiative.id === id) {
          initiative.has_voted = hasVoted
          initiative.vote_count += hasVoted ? 1 : -1
          break
        }
      }
    }
  }
}
</script>

<style scoped lang="scss">

.landing-title {
  p {
    font-size: 1.1rem;
    margin-bottom: 0.625rem;
  }
}

.action-card {
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;
  border-radius: 0.5rem;
  padding: 1rem 1rem 1rem 1.5rem;
  cursor: pointer;
  color: black;
  text-decoration: none;

  &:hover {
    background-color: white;
  }

  h6 {
    font-weight: 700;
    font-style: italic;
    text-transform: uppercase;
    letter-spacing: 0.1rem;
    line-height: 1;

    svg {
      height: 1.2rem;
      width: 1.2rem;
      margin-left: 0.5rem;
    }
  }

  p {
    font-size: 0.8rem;
    font-style: italic;
    line-height: 1.4;
    margin-bottom: 0;
  }
}

.action-cards {
  div:nth-child(2) .action-card-top {
    background-color: #8cade2;
  }
  div:nth-child(3) .action-card-top {
    background-color: #70b6a3;
  }
  div:nth-child(1) .action-card-top {
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
  height: 2.5rem;
  width: 2.5rem;
  right: 0.1rem;
  top: 0;
  display: flex;
  align-items: center;

  svg {
    height: 80%;
  }
}

.filter {
  box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
  border-radius: 1.5rem;
  border: 2px solid #f8f8f8;
  background-color: #f8f8f8;
  font-style: italic;
  font-size: 0.8rem;
  padding: 0.1rem 0.75rem;
  margin-left: 0.25rem;
  margin-top: 0.25rem;
  flex-wrap: wrap;

  &:hover {
    background-color: white;
    border-color: white;
  }

  @media (min-width: 576px) {
    margin-left: 0.5rem;
  }

  &.dropdown-open {
    border: 2px solid #ef7782;

    &:hover {
      border-color: #ef7782;
    }

    & > svg {
      transform: rotate(-180deg);
    }
  }

  & > svg {
    transition: transform 500ms;
    width: 0.5rem;
    height: 0.5rem;
  }

  .filter-dropdown {
    background-color: #f8f8f8;
    box-shadow: 0 0 2rem rgba(0, 0, 0, 0.2);
    border-radius: 0.5rem;
    top: 6rem;
    left: 2rem;
    right: 2rem;
    z-index: 15;
    padding: 1rem;
    text-align: left;
    cursor: default;
    max-height: 24rem;
    overflow-y: auto;

    @media (min-width: 768px) {
      top: 3rem;
    }

    @media (min-width: 992px) {
      left: auto;
      right: auto;
    }
  }
}

.initiatives-no {
  font-style: italic;
  font-size: 0.8rem;
}

.sort-initiatives {
  font-size: 0.8rem;
  box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
  background-color: #e8ebef;
  border-radius: 0.75rem;
  padding: 0.25rem 0.75rem;
  cursor: pointer;

  &:hover {
    background-color: #1A365D;
    color: white;

    svg {
      fill: white;
    }
  }

  svg {
    max-height: 0.7rem;
    max-width: 0.7rem;
    transition: transform 500ms;

    &.sort-ascending {
      transform: rotate(180deg);
    }
  }
}

.no-initiatives {
  background-color: #e8ebef;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 12rem;

  svg {
    max-width: 2rem;
    max-height: 2rem;
  }
}

#map-wrap {
  max-height: calc(100vh - 47px);
  position: sticky;
  top: 47px;
  z-index: 0;
}

</style>
