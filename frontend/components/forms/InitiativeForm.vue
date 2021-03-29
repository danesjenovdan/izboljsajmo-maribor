<template>
  <form
    enctype="multipart/form-data"
    @submit.prevent="createInitiative()"
  >
    <div class="form-group">
      <label for="initiative-title" class="mt-4">Naslov pobude*</label>
      <span
        v-if="errorInitiativeTitle"
        class="error-message"
      >
        Izpolnite polje.
      </span>
      <input
        id="initiative-title"
        v-model.trim="title"
        class="form-control"
        :class="{ 'error-input': errorInitiativeTitle }"
        name="initiative-title"
        placeholder="Vpišite naslov pobude"
        type="text"
      > <!-- @keyup="checkInitiativeTitle" -->
    </div>
    <div class="form-group">
      <div class="d-block">
        <label for="initiative-area" class="mt-4">Področje pobude*</label>
        <span v-if="errorInitiativeArea" class="error-message">
          Izpolnite polje.
        </span>
      </div>
      <b-form-select
        id="initiative-area"
        v-model="area"
        class="form-control"
        :class="{ 'error-input': errorInitiativeArea }"
        name="initiative-area"
        :options="initiativeAreaOptions"
      /> <!-- @change="checkInitiativeArea" -->
    </div>

    <div class="form-group">
      <label for="initiative-description" class="mt-4">Opis*</label>
      <!--
      <span v-if="errorInitiativeDescription" class="error-message">
        Izpolnite polje.
      </span>
      -->
      <textarea
        v-for="(description, index) in descriptions"
        :id="'initiative-description-' + index"
        :key="index"
        class="form-control mb-3"
        :placeholder="description"
        rows="5"
      />
    </div>

    <div class="form-group">
      <div class="d-block">
        <label for="initiative-location" class="mt-4">Lokacija*</label>
        <span v-if="errorInitiativeLocation" class="error-message">
          Izpolnite polje.
        </span>
      </div>
      <p class="form-note">
        Vpišite naslov ali povlecite žebljiček na lokacijo na zemljevidu.
      </p>
      <div class="d-inline-flex w-75 initiative-location-input">
        <input
          id="initiative-location"
          v-model="address"
          class="form-control"
          :class="{ 'error-input': errorInitiativeLocation }"
          name="initiative-location"
          type="text"
        > <!-- @keyup="checkInitiativeLocation" -->
        <b-button @click="findCoordinates">
          POTRDI
        </b-button>
      </div>
    </div>
    <div id="map-wrap" class="mt-4">
      <client-only>
        <l-map
          :zoom="13"
          :min-zoom="11"
          :center="[46.55465, 15.645881]"
          :max-bounds="[
            [46.46188844675249, 15.51583465730236],
            [46.62102957408261, 15.783283325506178]
          ]"
        >
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
        v-model="initiativeHasNoLocation"
        :aria-describedby="ariaDescribedby"
        @change="initiativeLocationEmpty"
      >
        Predlog nima lokacije.
      </b-form-checkbox>
    </b-form-group>
    <div class="form-group">
      <label class="mt-4">Naslovna slika*</label>
      <span v-if="errorCoverImage" class="error-message">
        Izpolnite polje.
      </span>
      <div :class="{ dropzone: true, 'drop-active': dropzone1Active }">
        <div v-if="coverImageFile || coverImageDraft">
          <div class="filenames">
            <span v-if="coverImageFile" class="mr-1">{{ coverImageFile.name }}</span>
            <span class="mr-1"><a v-if="coverImageDraft" :href="coverImageDraft.image" target="_blank">{{ coverImageDraft.id }}</a></span>
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
            <p>Dodajte sliko ali pa jo povlecite in odložite. Dovoljeni formati so: gif, jpg, png. Velikost naj ne presega 5 MB.</p>
          </div>
        </label>
      </div>
    </div>
    <div class="form-group">
      <label class="mt-4">Datoteke</label>
      <p class="form-note">
        Svoji pripombi lahko, če je to potrebno in primerno, dodate tudi fotografije oziroma druge datoteke, ki nam bodo v pomoč pri razumevanju pripombe.
      </p>
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
        {{ errorFormMessage }}
      </p>
    </div>
    <div v-if="errorUpload" class="text-center">
      <p class="error-message">
        {{ errorUploadMessage }}
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
</template>

<script>
export default {
  middleware: 'auth',
  props: {
    descriptions: {
      type: Array,
      default: () => []
    },
    errorDraft: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      id: -1,
      title: '',
      errorInitiativeTitle: false,
      area: null,
      errorInitiativeArea: false,
      initiativeAreaOptions: [{ value: null, text: 'Izberite področje' }],
      address: 'Maribor, Slovenija',
      mapMarkerPosition: {
        lat: 46.5576439,
        lng: 15.6455854
      },
      mapIcon: null,
      errorInitiativeLocation: false,
      initiativeHasNoLocation: false,
      coverImageFile: null,
      coverImageDraft: null,
      errorCoverImage: false,
      dropzone1Active: false,
      files: [],
      dropzone2Active: false,
      errorForm: false,
      errorFormMessage: 'Preverite, če so vsa polja izpolnjena.',
      errorUpload: false,
      errorUploadMessage: 'Prišlo je do napake pri oddaji predloga.'
    }
  },
  async created () {
    await this.fetchAreas()

    if (this.$route.query.id) {
      this.id = this.$route.query.id
      console.log('id', this.id)
      const response = await this.$axios.get(`v1/initiatives/${this.id}`)
      console.log(response)
      if (response.status === 200) {
        const initiative = response.data
        if (!initiative.is_draft) {
          return this.$router.push(`/predlogi/${this.id}`)
        }
        if (initiative.title) {
          this.title = initiative.title
        }
        if (initiative.area) {
          this.area = initiative.area.id
        }
        if (initiative.address) {
          this.address = initiative.address
        }
        if (initiative.location) {
          this.mapMarkerPosition.lat = initiative.location.coordinates[0]
          this.mapMarkerPosition.lng = initiative.location.coordinates[1]
        }
        // to do: naloadi cover image in files
        if (initiative.cover_image) {
          this.coverImageDraft = initiative.cover_image
        }
      }
    }
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
    // error checking
    checkInitiativeTitle () {
      this.errorInitiativeTitle = this.title.length === 0
    },
    checkInitiativeArea () {
      this.errorInitiativeArea = this.area === null
    },
    /*
    checkInitiativeDescription () {
      this.errorInitiativeDescription = this.form.initiativeDescription.length === 0
    },
    */
    checkCoverImage () {
      this.errorCoverImage = this.coverImageFile === null
    },
    async findCoordinates () {
      const response = await this.$axios.get(
        'https://nominatim.openstreetmap.org/search?',
        {
          params: {
            q: this.address,
            format: 'jsonv2',
            addressdetails: 1,
            countrycodes: 'si',
            'accept-language': 'sl'
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
      console.log(this.mapMarkerPosition)
      const response = await this.$axios.get(
        'https://nominatim.openstreetmap.org/reverse?',
        {
          params: {
            lat: this.mapMarkerPosition.lat,
            lon: this.mapMarkerPosition.lng,
            format: 'jsonv2',
            countrycodes: 'si',
            'accept-language': 'sl'
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
      if (!this.initiativeHasNoLocation) {
        this.errorInitiativeLocation = this.address.length === 0
      }
    },
    initiativeLocationEmpty () {
      if (this.initiativeHasNoLocation) {
        this.errorInitiativeLocation = false
      }
    },
    processCoverImage (event) {
      this.dropzone1Active = false
      const files = event.target.files || event.dataTransfer.files
      if (files) {
        this.coverImageDraft = null
        this.coverImageFile = files[0]
      }
      console.log(this.form)
    },
    removeCoverImage () {
      this.coverImageDraft = null
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
      this.errorUpload = false
      // this.errorForm = false

      const form = {}
      form.title = this.title
      form.area = this.area
      if (this.initiativeHasNoLocation) {
        form.location = null
        form.address = null
      } else {
        form.location = {
          type: 'Point',
          coordinates: [this.mapMarkerPosition.lat, this.mapMarkerPosition.lng]
        }
        form.address = this.address
      }
      // upload and set cover image
      if (this.coverImageFile) {
        const imageID = await this.$store.dispatch('postCoverImage', {
          image: this.coverImageFile
        })
        // if upload is unsuccessful, show error message and return
        if (imageID < 0) {
          this.errorUpload = true
          return
        }
        form.cover_image = {
          id: imageID
        }
      } else if (!this.coverImageDraft) { // it was reset to null
        form.cover_image = null
      }
      if (this.files.length > 0) {
        form.uploaded_files = []
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
          form.uploaded_files.push({
            id: filesID
          })
        }
      }

      this.$emit('create-draft', form, this.id)
    },
    async createInitiative () {
      this.errorUpload = false
      this.errorForm = false

      // check if there are errors in input fields
      this.checkInitiativeTitle()
      this.checkInitiativeArea()
      this.checkInitiativeLocation()
      this.checkCoverImage()

      // if everything is ok, start uploading
      if (
        !this.errorInitiativeTitle &&
        !this.errorInitiativeArea &&
        !this.errorInitiativeLocation &&
        !this.errorCoverImage
      ) {
        const form = {}
        form.title = this.title
        form.area = this.area
        if (!this.initiativeHasNoLocation) {
          form.location = {
            type: 'Point',
            coordinates: [this.mapMarkerPosition.lat, this.mapMarkerPosition.lng]
          }
          form.address = this.address
        }
        // upload and set cover image
        const imageID = await this.$store.dispatch('postCoverImage', {
          image: this.coverImageFile
        })
        // if upload is unsuccessful, show error message and return
        if (imageID < 0) {
          this.errorUpload = true
          return
        }
        form.cover_image = {
          id: imageID
        }
        console.log('img', imageID)
        // upload and set image files
        if (this.files.length > 0) {
          form.uploaded_files = []
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
            form.uploaded_files.push({
              id: filesID
            })
          }
        }
        console.log(form)
        this.$emit('create-initiative', form, this.id)
      } else {
        this.errorForm = true
      }
    }
  }
}
</script>

<style scoped lang="scss">

hr {
  width: calc(100% + 3rem);
  margin-left: -1.5rem;
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
