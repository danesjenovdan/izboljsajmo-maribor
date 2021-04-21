<template>
  <form enctype="multipart/form-data">
    <div class="form-group">
      <label for="initiative-title" class="mt-4">Naslov pobude*</label>
      <span
        v-if="showErrors && errorInitiativeTitle"
        class="error-message"
      >
        Izpolnite polje.
      </span>
      <p class="form-note">
        Maksimalna dolžina je 50 znakov.
      </p>
      <input
        id="initiative-title"
        v-model.trim="title"
        class="form-control"
        :class="{ 'error-input': showErrors && errorInitiativeTitle }"
        name="initiative-title"
        placeholder="Vpišite naslov pobude"
        type="text"
        maxlength="50"
      >
    </div>
    <div class="form-group">
      <div class="d-block">
        <label for="initiative-area" class="mt-4">Področje pobude*</label>
        <span v-if="showErrors && errorInitiativeArea" class="error-message">
          Izpolnite polje.
        </span>
      </div>
      <b-form-select
        id="initiative-area"
        v-model="area"
        class="form-control"
        :class="{ 'error-input': showErrors && errorInitiativeArea }"
        name="initiative-area"
        :options="initiativeAreaOptions"
      /> <!-- @change="checkInitiativeArea" -->
    </div>

    <div class="form-group">
      <label for="initiative-description" class="mt-4">Opis*</label>
      <span v-if="showErrors && errorInitiativeDescriptions" class="error-message">
        Izpolnite vsa polja.
      </span>
      <textarea
        v-for="description in descriptions"
        :id="description.field"
        :key="description.field"
        v-model="initiativeDescriptions[description.field]"
        class="form-control mb-3"
        :class="{ 'error-input': showErrors && !initiativeDescriptions[description.field] }"
        :placeholder="description.title"
        rows="5"
      />
    </div>

    <b-form-group v-if="hasSocialInnovativeIdeaCheckbox">
      <b-form-checkbox
        id="social-innovative-idea-checkbox"
        v-model="socialInnovativeIdea"
      >
        Je projekt družbeno koristen?
      </b-form-checkbox>
    </b-form-group>

    <div class="form-group">
      <div class="d-block">
        <label for="initiative-location" class="mt-4">Lokacija*</label>
        <span v-if="showErrors && errorInitiativeLocation" class="error-message">
          Izpolnite polje.
        </span>
      </div>
      <p class="form-note">
        Vpišite naslov ali povlecite žebljiček na lokacijo na zemljevidu.
      </p>
      <div class="d-sm-inline-flex initiative-location-input">
        <input
          id="initiative-location"
          v-model="address"
          class="form-control"
          :class="{ 'error-input': showErrors && errorInitiativeLocation }"
          name="initiative-location"
          type="text"
          maxlength="100"
        >
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
      >
        Predlog nima lokacije.
      </b-form-checkbox>
    </b-form-group>
    <div class="form-group">
      <label class="mt-4">Naslovna slika*</label>
      <span v-if="showErrors && errorCoverImage" class="error-message">
        Izpolnite polje.
      </span>
      <div :class="{ dropzone: true, 'drop-active': dropzone1Active }">
        <div v-if="coverImageFile || coverImageDraft">
          <div class="filenames">
            <span v-if="coverImageFile" class="mr-1">{{ coverImageFile.name }}</span>
            <span class="mr-1"><a v-if="coverImageDraft" :href="coverImageDraft.image" target="_blank">{{ coverImageDraft.id }}</a></span>
            <TrashcanIcon class="trashcan" @click="removeCoverImage" />
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
              <AddIcon />
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
        <div v-if="files.length > 0 || filesDraft.length > 0">
          <!-- draft files -->
          <div v-for="file in filesDraft" :key="file.name" class="filenames">
            <a :href="file.file" target="_blank"><span class="mr-1">{{ file.name }}</span></a>
            <TrashcanIcon class="trashcan" @click="removeFileDraft(file.name)" />
          </div>
          <!-- uploaded files -->
          <div v-for="file in files" :key="file.name" class="filenames">
            <span class="mr-1">{{ file.name }}</span>
            <TrashcanIcon class="trashcan" @click="removeFile(file.name)" />
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
            accept="image/*,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            @change="processFiles($event)"
          >
          <div class="d-flex align-items-center">
            <div class="drop-circle btn d-flex justify-content-center align-items-center">
              <AddIcon />
            </div>
            <p>Dodaj datoteke ali pa jih povleci in odloži. Dovoljeni formati so: gif, jpg, png, doc, docx, pdf, odt. Velikost naj ne presega 5 MB.</p>
          </div>
        </label>
      </div>
    </div>
    <hr class="hr-upper">
    <hr class="hr-lower">
    <p v-if="errorMessage" class="message d-flex justify-content-center align-items-center position-relative">
      <IconDanger />{{ errorMessageText }}
      <span class="position-absolute" @click="closeErrorMessage">Zapri</span>
    </p>
    <p v-if="successMessage" class="message d-flex justify-content-center align-items-center position-relative">
      <IconSuccess />{{ successMessageText }}
      <span class="position-absolute" @click="closeSuccessMessage">Zapri</span>
    </p>
    <div class="d-flex justify-content-between align-items-center">
      <div class="d-flex">
        <button
          type="button"
          class="save-button"
          @click="createDraft"
        >
          Shrani
        </button>
        <button
          class="cancel-button"
          type="button"
          @click="deleteInitiative"
        >
          Zavrzi
        </button>
      </div>
      <b-button
        type="button"
        class="d-flex align-items-center pl-4 pr-3"
        :class="{ 'submit-button-disabled': !noErrors }"
        @click="submitForm"
      >
        <span class="mr-4">ODDAJ</span>
        <ArrowRightIcon />
      </b-button>
    </div>
  </form>
</template>

<script>
import TrashcanIcon from '~/assets/img/icons/trashcan.svg?inline'
import AddIcon from '~/assets/img/icons/add.svg?inline'
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'
import IconDanger from '~/assets/img/icons/danger.svg?inline'
import IconSuccess from '~/assets/img/icons/success.svg?inline'

export default {
  components: { TrashcanIcon, AddIcon, ArrowRightIcon, IconDanger, IconSuccess },
  middleware: 'auth',
  props: {
    descriptions: {
      type: Array,
      default: () => []
    },
    errorMessage: {
      type: Boolean,
      default: false
    },
    errorMessageText: {
      type: String,
      default: ''
    },
    successMessage: {
      type: Boolean,
      default: false
    },
    successMessageText: {
      type: String,
      default: ''
    },
    hasSocialInnovativeIdeaCheckbox: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      id: -1,
      title: '',
      area: null,
      initiativeAreaOptions: [{ value: null, text: 'Izberite področje' }],
      initiativeDescriptions: {},
      socialInnovativeIdea: false,
      address: 'Maribor, Slovenija',
      mapMarkerPosition: {
        lat: 46.5576439,
        lng: 15.6455854
      },
      mapIcon: null,
      initiativeHasNoLocation: false,
      coverImageFile: null,
      coverImageDraft: null,
      dropzone1Active: false,
      files: [],
      filesDraft: [],
      dropzone2Active: false,
      showErrors: false
    }
  },
  computed: {
    errorInitiativeTitle () {
      return !(this.title.length > 0 && this.title.length <= 50)
    },
    errorInitiativeArea () {
      return this.area === null
    },
    errorInitiativeDescriptions () {
      if (Object.keys(this.initiativeDescriptions).length === this.descriptions.length) {
        for (const desc in this.initiativeDescriptions) {
          if (this.initiativeDescriptions[desc] === '') {
            return true
          }
        }
        return false
      }
      return true
    },
    errorInitiativeLocation () {
      return !this.initiativeHasNoLocation && this.address.length === 0
    },
    errorCoverImage () {
      return this.coverImageFile === null && this.coverImageDraft === null
    },
    noErrors () {
      return !this.errorInitiativeTitle && !this.errorInitiativeArea && !this.errorInitiativeLocation && !this.errorCoverImage && !this.errorInitiativeDescriptions
    }
  },
  watch: {
    successMessage () {
      if (this.successMessage) {
        this.resetForm()
      }
    }
  },
  async created () {
    await this.fetchAreas()

    if (this.$route.query.id) {
      this.id = this.$route.query.id
      // console.log('id', this.id)
      const response = await this.$axios.get(`v1/initiatives/${this.id}`)
      // console.log(response)
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
        if (initiative.descriptions) {
          for (const desc of initiative.descriptions) {
            this.initiativeDescriptions[desc.field] = desc.content
          }
        }
        if (initiative.is_social_inovative_idea) {
          this.socialInnovativeIdea = true
        }
        if (initiative.address) {
          this.address = initiative.address
        } else {
          this.initiativeHasNoLocation = true
        }
        if (initiative.location) {
          this.mapMarkerPosition.lat = initiative.location.coordinates[0]
          this.mapMarkerPosition.lng = initiative.location.coordinates[1]
        } else {
          this.mapMarkerPosition.lat = 46.5576439
          this.mapMarkerPosition.lng = 15.6455854
        }
        if (initiative.cover_image) {
          this.coverImageDraft = initiative.cover_image
        }
        if (initiative.uploaded_files) {
          for (const file of initiative.uploaded_files) {
            this.filesDraft.push(file)
          }
        }
      }
    }
  },
  methods: {
    resetForm () {
      // hide error messages
      this.showErrors = false
      // reset fields
      this.title = ''
      this.area = null
      this.initiativeDescriptions = {}
      this.socialInnovativeIdea = false
      this.address = 'Maribor, Slovenija'
      this.mapMarkerPosition.lat = 46.5576439
      this.mapMarkerPosition.lng = 15.6455854
      this.initiativeHasNoLocation = false
      this.removeCoverImage()
      this.files = []
      this.filesDraft = []
    },
    setIconStyles () {
      this.mapIcon = this.$L.icon({
        iconUrl: require('@/assets/img/icons/pin.svg'),
        iconSize: [32, 32]
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
    closeErrorMessage () {
      this.$emit('close-error-message')
    },
    closeSuccessMessage () {
      this.$emit('close-success-message')
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
      // console.log(this.mapMarkerPosition)
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
    processCoverImage (event) {
      this.dropzone1Active = false
      const files = event.target.files || event.dataTransfer.files
      if (files) {
        this.coverImageDraft = null
        this.coverImageFile = files[0]
      }
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
    },
    removeFile (filename) {
      for (let i = 0; i < this.files.length; i++) {
        if (this.files[i].name === filename) {
          this.files.splice(i, 1)
        }
      }
    },
    removeFileDraft (filename) {
      for (let i = 0; i < this.filesDraft.length; i++) {
        if (this.filesDraft[i].name === filename) {
          this.filesDraft.splice(i, 1)
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
    deleteInitiative () {
      if (confirm('Ali ste prepričani, da želite izbrisati ta predlog?')) {
        this.$emit('delete-initiative', this.id)
      }
    },
    async createDraft () {
      try {
        const form = {}
        form.title = this.title
        form.area = this.area
        form.descriptions = []
        for (const desc of this.descriptions) {
          if (this.initiativeDescriptions[desc.field]) {
            form.descriptions.push({
              title: desc.title,
              field: desc.field,
              content: this.initiativeDescriptions[desc.field]
            })
          }
        }
        if (this.hasSocialInnovativeIdeaCheckbox) {
          form.is_social_inovative_idea = this.socialInnovativeIdea
        }
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
          form.cover_image = {
            id: imageID
          }
        } else if (!this.coverImageDraft) { // it was reset to null or never set
          form.cover_image = null
        }
        // upload and set files
        form.uploaded_files = []
        if (this.filesDraft.length > 0) {
          for (const file of this.filesDraft) {
            form.uploaded_files.push({
              id: file.id
            })
          }
        }
        if (this.files.length > 0) {
          for (let i = 0; i < this.files.length; i++) {
            const filesID = await this.$store.dispatch('postFiles', {
              file: this.files[i],
              name: this.files[i].name
            })
            form.uploaded_files.push({
              id: filesID
            })
          }
        }
        // console.log(form)
        this.$emit('create-draft', form, this.id)
      } catch {
        this.$emit('on-error')
      }
    },
    submitForm () {
      if (this.noErrors) {
        this.createInitiative()
      } else {
        this.showErrors = true
      }
    },
    async createInitiative () {
      try {
        const form = {}
        form.title = this.title
        form.area = this.area
        form.descriptions = []
        for (const desc of this.descriptions) {
          form.descriptions.push({
            title: desc.title,
            field: desc.field,
            content: this.initiativeDescriptions[desc.field]
          })
        }
        if (this.hasSocialInnovativeIdeaCheckbox) {
          form.is_social_inovative_idea = this.socialInnovativeIdea
        }
        if (!this.initiativeHasNoLocation) {
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
          form.cover_image = {
            id: imageID
          }
        }
        // upload and set files
        form.uploaded_files = []
        if (this.filesDraft.length > 0) {
          for (const file of this.filesDraft) {
            form.uploaded_files.push({
              id: file.id
            })
          }
        }
        if (this.files.length > 0) {
          for (let i = 0; i < this.files.length; i++) {
            const filesID = await this.$store.dispatch('postFiles', {
              file: this.files[i],
              name: this.files[i].name
            })
            form.uploaded_files.push({
              id: filesID
            })
          }
        }
        // console.log(form)
        this.$emit('create-initiative', form, this.id)
      } catch {
        this.$emit('on-error')
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
  @media (min-width: 576px) {
    width: 100%;
  }
  @media (min-width: 768px) {
    width: 75%;
  }
  button {
    width: 100%;
    font-size: 0.8rem;

    @media (min-width: 576px) {
      width: unset;
      margin: 0 1rem;
      padding: 0.4rem 1rem;
    }

  }
}

#map-wrap {
  height: 20rem;
}

.trashcan {
  cursor: pointer;
  max-height: 1.25rem;
  max-width: 1.25rem;
}

.save-button,
.cancel-button {
  border: none;
  background-color: unset;
  font-size: 1rem;
  text-decoration: underline;
  margin-right: 0.5rem;

  &:hover {
    color: white;
  }

  @media (min-width: 576px) {
    font-size: 0.8rem;
    text-decoration: none;
    border-radius: 1rem;
    box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
    padding: 0.4rem 1.5rem;
  }
}

.save-button {
  margin-right: 1rem;
  @media (min-width: 576px) {
    background-color: #ef7782;
    &:hover {
      background-color: #1A365D;
    }
  }
}

.cancel-button {
  @media (min-width: 576px) {
    background-color: #d7d7d7;
    &:hover {
      background-color: #1A365D;
    }
  }
}

.submit-button-disabled {
  background-color: grey;
}

</style>
