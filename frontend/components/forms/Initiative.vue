<template>
  <div>
    <div
      class="form-top"
      :class="{
        'form-top-mm': initiativeType === 'MM',
        'form-top-ii': initiativeType === 'II',
        'form-top-zm': initiativeType === 'ZM',
      }"
    />
    <div class="initiative-form">
      <form
        enctype="multipart/form-data"
        @submit.prevent="createInitiative()"
      >
        <h4>{{ formTitle }}</h4>
        <p class="form-subtitle">
          Naznani okvare, poškodbe, slabosti (pomanjkljivosti), ki jih zaznavaš v svojem okolju.
        </p>
        <div class="form-group">
          <label for="initiative-title" class="mt-4">Naslov pobude*</label>
          <span
            v-if="errorInitiativeTitle"
            class="error-message"
          >
            Vpiši naslov pobude.
          </span>
          <input
            id="initiative-title"
            v-model.trim="title"
            :class="{ 'form-control': true, 'error-input': errorInitiativeTitle }"
            name="initiative-title"
            type="text"
            required
            @keyup="checkInitiativeTitle"
          >
        </div>
        <div class="form-group">
          <div class="d-block">
            <label for="initiative-area" class="mt-4">Področje pobude*</label>
            <span v-if="errorInitiativeArea" class="error-message">
              Izberi področje pobude.
            </span>
          </div>
          <b-form-select
            id="initiative-area"
            v-model="area"
            :class="{ 'form-control': true, 'error-input': errorInitiativeArea }"
            name="initiative-area"
            :options="initiativeAreaOptions"
            @change="checkInitiativeArea"
          />
        </div>
        <div class="form-group">
          <label for="initiative-description" class="mt-4">Opis*</label>
          <span v-if="errorInitiativeDescription" class="error-message">
            Vpiši opis pobude.
          </span>
          <textarea
            id="initiative-description"
            v-model.trim="description"
            :class="{ 'form-control': true, 'error-input': errorInitiativeDescription }"
            placeholder="Na katero težavo, pomanjkljivost, napako, okvaro, nevarnost se nanaša vaša pobuda?"
            rows="5"
            required
            @keyup="checkInitiativeDescription"
          />
        </div>
        <b-form-group class="mt-4">
          <b-form-textarea
            id="initiative-suggestion"
            v-model.trim="suggestion"
            :class="{ 'form-control': true }"
            placeholder="Kakšen je vaš predlog rešitve, odprave pomanjkljivosti/slabosti?"
            rows="5"
          />
        </b-form-group>
        <div class="form-group">
          <div class="d-block">
            <label for="initiative-location" class="mt-4">Lokacija*</label>
            <span v-if="errorInitiativeLocation" class="error-message">Vpiši lokacijo pobude.</span>
          </div>
          <p class="form-note">
            Vpiši naslov ali povleci marker na lokacijo na zemljevidu.
          </p>
          <div class="d-inline-flex w-75 initiative-location-input">
            <input
              id="initiative-location"
              v-model="address"
              :class="{ 'form-control': true, 'error-input': errorInitiativeLocation }"
              name="initiative-location"
              type="text"
              required
              @keyup="checkInitiativeLocation"
            >
            <b-button @click="findCoordinates">
              POTRDI
            </b-button>
          </div>
        </div>
        <div id="map-wrap" class="mt-4">
          <client-only>
            <l-map :zoom="13" :center="[46.55465, 15.645881]">
              <l-tile-layer
                url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
              />
              <l-marker
                :lat-lng.sync="mapMarkerPosition"
                :draggable="true"
                :icon="mapIcon"
                @ready="setIconStyles"
                @dragend="findAddress"
              >
                <l-popup>{{ address }}</l-popup>
              </l-marker>
            </l-map>
          </client-only>
        </div>
        <b-form-group v-slot="{ ariaDescribedby }">
          <b-form-checkbox
            id="no-location-allowed"
            v-model="initiativeLocationIsEmpty"
            :aria-describedby="ariaDescribedby"
            @change="initiativeLocationEmpty"
          >
            Predlog nima lokacije.
          </b-form-checkbox>
        </b-form-group>
        <div class="form-group">
          <label class="mt-4">Naslovna slika*</label>
          <div :class="{ dropzone: true, 'drop-active': dropzone1Active }">
            <div v-if="coverImageFile">
              <div class="filenames">
                <span class="mr-1">{{ coverImageFile.name }}</span>
                <img
                  src="~/assets/img/icons/trashcan.svg"
                  alt="trashcan"
                  class="trashcan"
                  @click="removeCoverImage"
                >
              </div>
              <hr class="hr-upper">
              <hr class="hr-lower">
            </div>
            <label
              for="initiative-cover-image"
              @drop.prevent="processCoverImage($event)"
              @dragover.prevent="dragOverHandler1"
              @dragenter.prevent=""
              @dragleave.prevent="dragLeaveHandler1"
            >
              <input
                id="initiative-cover-image"
                ref="coverImageFile"
                name="initiative-cover-image"
                type="file"
                class="d-none"
                accept="image/*"
                @change="processCoverImage($event)"
              >
              <div class="d-flex align-items-center">
                <div class="drop-circle btn d-flex justify-content-center align-items-center">
                  <img src="~/assets/img/icons/add.svg" alt="add">
                </div>
                <p>Dodaj sliko ali pa jo povleci in odloži. Dovoljeni formati so: gif, jpg, png. Velikost naj ne presega 5 MB.</p>
              </div>
            </label>
          </div>
        </div>
        <div class="form-group">
          <label class="mt-4">Datoteke</label>
          <div :class="{ dropzone: true, 'drop-active': dropzone2Active }">
            <div v-if="files.length > 0">
              <div v-for="file in files" :key="file.name" class="filenames">
                <span class="mr-1">{{ file.name }}</span>
                <img
                  src="~/assets/img/icons/trashcan.svg"
                  alt="trashcan"
                  class="trashcan"
                  @click="removeFile(file.name)"
                >
              </div>
              <hr class="hr-upper">
              <hr class="hr-lower">
            </div>
            <label
              for="initiative-files"
              @drop.prevent="processFiles($event)"
              @dragover.prevent="dragOverHandler2"
              @dragenter.prevent=""
              @dragleave.prevent="dragLeaveHandler2"
            >
              <input
                id="initiative-files"
                ref="files"
                name="initiative-files"
                type="file"
                class="d-none"
                multiple
                accept="image/*"
                @change="processFiles($event)"
              >
              <div class="d-flex align-items-center">
                <div class="drop-circle btn d-flex justify-content-center align-items-center">
                  <img src="~/assets/img/icons/add.svg" alt="add">
                </div>
                <p>Dodaj datoteke ali pa jih povleci in odloži. Dovoljeni formati so: gif, jpg, png, doc, docx, pdf, odt. Velikost naj ne presega 5 MB.</p>
              </div>
            </label>
          </div>
        </div>
        <hr class="hr-upper">
        <hr class="hr-lower">
        <div v-if="errorForm" class="text-center">
          <p class="error-message">
            Obrazec ni pravilno izpolnjen.
          </p>
        </div>
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <b-button class="save-button px-4" @click="createDraft()">
              Shrani
            </b-button>
            <b-button
              class="cancel-button px-4 ml-2"
              @click="$router.push('/predlogi')"
            >
              Zavrzi
            </b-button>
          </div>
          <b-button type="submit" class="d-flex align-items-center pl-4 pr-3">
            <span class="mr-4">ODDAJ</span>
            <img src="~/assets/img/icons/arrow-right.svg" alt="arrow right">
          </b-button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  middleware: 'auth',
  props: {
    initiativeType: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      title: '',
      area: null,
      description: '',
      suggestion: '',
      coverImageFile: null,
      files: [],
      errorInitiativeTitle: false,
      initiativeAreaOptions: [{ value: null, text: 'Izberite področje' }],
      errorInitiativeArea: false,
      errorInitiativeDescription: false,
      address: 'Maribor, Slovenija',
      errorInitiativeLocation: false,
      initiativeLocationIsEmpty: false,
      dropzone1Active: false,
      dropzone2Active: false,
      errorForm: false,
      mapMarkerPosition: {
        lat: 46.5576439,
        lng: 15.6455854
      },
      mapIcon: null
    }
  },
  computed: {
    formTitle () {
      return this.$store.getters.initiativeTypes[this.initiativeType]
    },
    form () {
      return {
        initiativeTitle: this.title,
        initiativeArea: this.area,
        initiativeDescription: this.description,
        initiativeSuggestion: this.suggestion,
        initiativeAddress: this.address,
        initiativeLocation: {
          type: 'Point',
          coordinates: [this.mapMarkerPosition.lat, this.mapMarkerPosition.lng]
        },
        initiativeCoverImage: '',
        initiativeFiles: []
      }
    }
  },
  created () {
    this.fetchAreas()
  },
  methods: {
    setIconStyles () {
      this.mapIcon = this.$L.icon({
        iconUrl: require('@/assets/img/icons/pin.svg')
      })
    },
    async fetchAreas () {
      const areas = await this.$store.dispatch('getAreas')
      for (const i in areas) {
        this.initiativeAreaOptions.push({
          value: areas[i].id,
          text: areas[i].name
        })
      }
    },
    checkInitiativeTitle () {
      this.errorInitiativeTitle = this.title.length === 0
    },
    checkInitiativeArea () {
      this.errorInitiativeArea = this.area === null
    },
    checkInitiativeDescription () {
      this.errorInitiativeDescription = this.form.initiativeDescription.length === 0
    },
    async findCoordinates () {
      const response = await this.$axios.get(
        'https://nominatim.openstreetmap.org/search?',
        {
          params: {
            q: this.form.initiativeAddress,
            city: 'Maribor',
            country: 'Slovenia',
            postalcode: 2000,
            countrycodes: 'si',
            accept_language: 'sl'
          }
        }
      )
      if (response.status === 200) {
        if (response.data.length > 0) {
          const location = response.data[0]
          this.address = this.formatAddress(location.address)
          this.mapMarkerPosition = {
            lat: location.lat,
            lng: location.lon
          }
        }
      }
    },
    async findAddress () {
      const response = await this.$axios.get(
        'https://nominatim.openstreetmap.org/reverse?',
        {
          params: {
            lat: this.mapMarkerPosition.lat,
            lon: this.mapMarkerPosition.lng,
            format: 'jsonv2',
            countrycodes: 'si',
            accept_language: 'sl'
          }
        }
      )
      if (response.status === 200) {
        this.address = this.formatAddress(response.data.address)
      }
    },
    formatAddress (address) {
      // {"house_number":"7","road":"Ulica heroja Zidanška","suburb":"Tabor","city_district":"Maribor","city":"Maribor","postcode":"2000","country":"Slovenija","country_code":"si"}
      const streetAndHouseNo = (address.road) ? (address.house_number ? `${address.road} ${address.house_number}, ` : `${address.road}, `) : ''
      const city = address.city || address.town || address.village || address.municipality || ''
      const postcodeAndCity = `${address.postcode} ${city}, `
      return `${streetAndHouseNo}${postcodeAndCity}${address.country}`
    },
    checkInitiativeLocation () {
      if (!this.initiativeLocationIsEmpty) {
        this.errorInitiativeLocation = this.form.initiativeAddress.length === 0
      }
    },
    initiativeLocationEmpty () {
      if (this.initiativeLocationIsEmpty) {
        this.errorInitiativeLocation = false
      }
    },
    processCoverImage (event) {
      this.dropzone1Active = false
      const files = event.target.files || event.dataTransfer.files
      if (files) {
        this.coverImageFile = files[0]
      }
      console.log(this.form)
    },
    removeCoverImage () {
      this.coverImageFile = null
    },
    processFiles (event) {
      this.dropzone2Active = false
      const files = event.target.files || event.dataTransfer.files
      for (let f = 0; f < files.length; f++) {
        this.files.push(files[f])
      }
      console.log(this.form)
    },
    removeFile (filename) {
      for (let i = 0; i < this.files.length; i++) {
        if (this.files[i].name === filename) {
          this.files.splice(i, 1)
        }
      }
    },
    dragOverHandler1 () {
      this.dropzone1Active = true
    },
    dragLeaveHandler1 () {
      this.dropzone1Active = false
    },
    dragOverHandler2 () {
      this.dropzone2Active = true
    },
    dragLeaveHandler2 () {
      this.dropzone2Active = false
    },
    async createDraft () {
      try {
        // is draft
        this.form.isDraft = true
        // add initiative type
        this.form.initiativeType = this.initiativeType
        // upload and set cover image
        if (this.coverImageFile) {
          const imageID = await this.$store.dispatch('postCoverImage', {
            image: this.coverImageFile
          })
          this.form.initiativeCoverImage = {
            id: imageID
          }
        }
        // upload and set image files
        for (let i = 0; i < this.files.length; i++) {
          console.log({
            file: this.files[i],
            name: this.files[i].name
          })
          const filesID = await this.$store.dispatch('postFiles', {
            file: this.files[i],
            name: this.files[i].name
          })
          this.form.initiativeFiles.push({
            id: filesID
          })
        }
        // remove location if empty
        if (this.initiativeLocationIsEmpty) {
          this.form.initiativeLocation = null
          this.form.initiativeAddress = null
        }
        console.log(this.form)
        await this.$store.dispatch('postInitiative', this.form)
        await this.$router.push('/')
      } catch (err) {
        // this.errorComment = true
        console.log(err)
      }
    },
    async createInitiative () {
      if (
        !this.errorInitiativeTitle &&
        !this.errorInitiativeArea &&
        !this.errorInitiativeDescription &&
        !this.errorInitiativeLocation &&
        this.coverImageFile
      ) {
        try {
          // upload and set cover image
          const imageID = await this.$store.dispatch('postCoverImage', {
            image: this.coverImageFile
          })
          this.form.initiativeCoverImage = {
            id: imageID
          }
          console.log('img', imageID)
          // upload and set image files
          for (let i = 0; i < this.files.length; i++) {
            console.log({
              file: this.files[i],
              name: this.files[i].name
            })
            const filesID = await this.$store.dispatch('postFiles', {
              file: this.files[i],
              name: this.files[i].name
            })
            this.form.initiativeFiles.push({
              id: filesID
            })
          }
          // remove location if empty
          if (this.initiativeLocationIsEmpty) {
            this.form.initiativeLocation = null
            this.form.initiativeAddress = null
          }
          // add initiative type
          this.form.initiativeType = this.initiativeType
          console.log(this.form)
          const id = await this.$store.dispatch('postInitiative', this.form)
          await this.$router.push(`/predlogi/${id}`)
        } catch (err) {
          // this.errorComment = true
          console.log(err)
        }
      } else {
        this.errorForm = true
      }
    }
  }
}
</script>

<style scoped lang="scss">
.initiative-form {
  box-shadow: 4px 4px 11px #d4d9e1, -5px -5px 11px #ffffff;
  border-radius: 0.5rem;
  margin: 3rem 0;
  padding: 2.5rem 1.5rem;
}

.form-top {
  height: 1rem;
  width: calc(100% - 30px);
  position: absolute;
  top: 3rem;
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;

  &.form-top-mm {
    background-color: #8cade2;
  }

  &.form-top-ii {
    background-color: #70b6a3;
  }

  &.form-top-zm {
    background-color: #d9ab27;
  }
}

h4 {
  font-weight: 700;
  font-style: italic;
  letter-spacing: 2.4px;
  margin-bottom: 0;
}

hr {
  width: calc(100% + 3rem);
  margin-left: -1.5rem;
}

.form-subtitle {
  margin-bottom: 2rem;
  font-style: italic;
}

.initiative-location-input {
  button {
    margin: 0 1rem;
  }
}

#map-wrap {
  height: 20rem;
}

.trashcan {
  cursor: pointer;
}

.save-button,
.cancel-button {
  font-size: 0.8rem;
  font-style: normal;
  font-weight: normal;
  letter-spacing: normal;
}

.cancel-button {
  background-color: #d7d7d7;
  &:hover {
    background-color: #6c757d;
  }
}
</style>
