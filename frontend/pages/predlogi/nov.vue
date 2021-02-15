<template>
  <b-container fluid>
    <b-row class="justify-content-center">
      <b-col cols="12" md="10" lg="6" class="position-relative">
        <div class="form-top" />
        <div class="initiative-form">
          <form enctype="multipart/form-data" @submit.prevent="createInitiative">
            <h4>MOTI ME!</h4>
            <p class="form-subtitle">
              Naznani okvare, poškodbe, slabosti (pomanjkljivosti), ki jih zaznavaš v svojem okolju.
            </p>
            <div class="form-group">
              <label for="initiative-title" class="mt-4">Naslov pobude*</label>
              <span v-if="errorInitiativeTitle" class="error-message">Vpiši naslov pobude.</span>
              <input
                id="initiative-title"
                v-model.trim="form.initiativeTitle"
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
                <span v-if="errorInitiativeArea" class="error-message">Izberi področje pobude.</span>
              </div>
              <b-form-select
                id="initiative-area"
                v-model="form.initiativeArea"
                :class="{ 'form-control': true, 'error-input': errorInitiativeArea }"
                name="initiative-area"
                :options="initiativeAreaOptions"
                @change="checkInitiativeArea"
              />
            </div>
            <div class="form-group">
              <label for="initiative-description" class="mt-4">Opis*</label>
              <span v-if="errorInitiativeDescription" class="error-message">Vpiši opis pobude.</span>
              <textarea
                id="initiative-description"
                v-model.trim="form.initiativeDescription"
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
                v-model.trim="form.initiativeSuggestion"
                :class="{ 'form-control': true}"
                placeholder="Kakšen je vaš predlog rešitve, odprave pomanjkljivosti/slabosti?"
                rows="5"
              /> <!-- @keyup="checkInitiativeSuggestion" -->
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
                  v-model.trim="form.initiativeLocation"
                  :class="{ 'form-control': true, 'error-input': errorInitiativeLocation }"
                  name="initiative-location"
                  type="text"
                  required
                  @keyup="checkInitiativeLocation"
                >
                <b-button
                  @click="findLocation"
                >
                  POTRDI
                </b-button>
              </div>
            </div>
            <img src="~/static/map.png" class="map img-fluid my-4">
            <b-form-group v-slot="{ ariaDescribedby }">
              <b-form-checkbox
                id="no-location-allowed"
                v-model="initiativeLocationEmptyAllowed"
                :aria-describedby="ariaDescribedby"
                @change="initiativeLocationEmpty"
              >
                Predlog nima lokacije.
              </b-form-checkbox>
            </b-form-group>
            <div class="form-group">
              <label class="mt-4">Naslovna slika*</label>
              <div :class="{'dropzone': true, 'drop-active': dropzone1Active}">
                <div v-if="form.coverImageFile">
                  <div class="filenames">
                    <span class="mr-1">{{ form.coverImageFile.name }}</span>
                    <img
                      src="~/assets/img/icons/trashcan.png"
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
                    required
                    accept="image/*"
                    @change="processCoverImage($event)"
                  >
                  <div class="d-flex align-items-center">
                    <b-button class="drop-circle d-flex justify-content-center align-items-center">
                      <img src="~/assets/img/icons/add.png" alt="add">
                    </b-button>
                    <p>
                      Dodaj sliko ali pa jo povleci in odloži. Dovoljeni formati so: gif, jpg, png. Velikost naj ne presega 5 MB.
                    </p>
                  </div>
                </label>
              </div>
            </div>
            <div class="form-group">
              <label class="mt-4">Datoteke</label>
              <div :class="{'dropzone': true, 'drop-active': dropzone2Active}">
                <div v-if="form.files.length > 0">
                  <div v-for="file in form.files" :key="file.name" class="filenames">
                    <span class="mr-1">{{ file.name }}</span>
                    <img
                      src="~/assets/img/icons/trashcan.png"
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
                  @drop.prevent="processFiles($event);"
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
                    <b-button class="drop-circle d-flex justify-content-center align-items-center">
                      <img src="~/assets/img/icons/add.png" alt="add">
                    </b-button>
                    <p>
                      Dodaj datoteke ali pa jih povleci in odloži. Dovoljeni formati so: gif, jpg, png, doc, docx, pdf, odt.
                      Velikost naj ne presega 5 MB.
                    </p>
                  </div>
                </label>
              </div>
            </div>
            <hr class="hr-upper">
            <hr class="hr-lower">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <b-button class="save-button px-4">
                  Shrani
                </b-button>
                <b-button class="cancel-button px-4 ml-2">
                  Zavrzi
                </b-button>
              </div>
              <b-button type="submit" class="d-flex align-items-center px-4">
                <span class="mr-4">ODDAJ</span>
                <img src="~/assets/img/icons/arrow-right.png" alt="arrow right">
              </b-button>
            </div>
          </form>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data () {
    return {
      form: {
        initiativeTitle: '',
        initiativeArea: null,
        initiativeDescription: '',
        initiativeSuggestion: '',
        initiativeLocation: '',
        coverImageFile: null,
        files: []
      },
      errorInitiativeTitle: false,
      initiativeAreaOptions: [
        { value: null, text: 'Izberite področje' }
      ],
      errorInitiativeArea: false,
      errorInitiativeDescription: false,
      errorInitiativeLocation: false,
      initiativeLocationEmptyAllowed: false,
      dropzone1Active: false,
      dropzone2Active: false
    }
  },
  created () {
    this.fetchAreas()
  },
  methods: {
    async fetchAreas () {
      const response = await this.$axios.get('v1/areas/')
      const responseData = await response.data
      if (response.status === 200) {
        for (const i in responseData) {
          this.initiativeAreaOptions.push({
            value: responseData[i].id,
            text: responseData[i].name
          })
        }
      } else {
        // console.log('ni ok', responseData)
        // throw error
      }
    },
    checkInitiativeTitle () {
      this.errorInitiativeTitle = this.form.initiativeTitle.length === 0
    },
    checkInitiativeArea () {
      this.errorInitiativeArea = this.form.initiativeArea === null
    },
    checkInitiativeDescription () {
      this.errorInitiativeDescription = this.form.initiativeDescription.length === 0
    },
    checkInitiativeLocation () {
      if (!this.initiativeLocationEmptyAllowed) {
        this.errorInitiativeLocation = this.form.initiativeLocation.length === 0
      }
    },
    initiativeLocationEmpty () {
      if (this.initiativeLocationEmptyAllowed) {
        this.errorInitiativeLocation = false
      }
    },
    findLocation () {
      this.form.initiativeLocation = {
        type: 'Point',
        coordinates: [-123.0208, 44.0464]
      }
    },
    processCoverImage (event) {
      this.dropzone1Active = false
      const files = event.target.files || event.dataTransfer.files
      if (files) {
        this.form.coverImageFile = files[0]
      }
      console.log(this.form)
    },
    removeCoverImage () {
      this.form.coverImageFile = null
    },
    processFiles (event) {
      this.dropzone2Active = false
      const files = event.target.files || event.dataTransfer.files
      for (let f = 0; f < files.length; f++) {
        this.form.files.push(files[f])
      }
      console.log(this.form)
    },
    removeFile (filename) {
      for (let i = 0; i < this.form.files.length; i++) {
        if (this.form.files[i].name === filename) {
          this.form.files.splice(i, 1)
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
    async createInitiative () {
      console.log(JSON.stringify(this.form))
      if (!this.errorInitiativeTitle &&
        !this.errorInitiativeArea &&
        !this.errorInitiativeDescription &&
        !this.errorInitiativeLocation) {
        try {
          await this.$store.dispatch('postInitiative', this.form)
        } catch (err) {
          // this.errorComment = true
          console.log(err)
        }
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
  background-color: #8cade2;
  height: 1rem;
  width: calc(100% - 30px);
  position: absolute;
  top: 3rem;
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
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

.trashcan {
  cursor: pointer;
}

.save-button, .cancel-button {
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
