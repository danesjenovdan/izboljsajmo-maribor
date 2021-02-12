<template>
  <b-container fluid>
    <b-row class="justify-content-center">
      <b-col cols="6" class="position-relative">
        <div class="form-top" />
        <div class="initiative-form">
          <form enctype="multipart/form-data" @submit.prevent="createInitiative">
            <h4>MOTI ME!</h4>
            <p class="form-subtitle">
              Naznani okvare, poškodbe, slabosti (pomanjkljivosti), ki jih zaznavaš v svojem okolju.
            </p>
            <div class="form-group">
              <label for="initiative-title">Naslov pobude*</label>
              <span v-if="errorInitiativeTitle" class="error-message">Vpiši naslov pobude.</span>
              <input
                id="initiative-title"
                v-model.trim="initiativeTitle"
                :class="{ 'form-control': true, 'error-input': errorInitiativeTitle }"
                name="initiative-title"
                type="text"
                required
                @blur="checkInitiativeTitle"
              >
            </div>
            <div class="form-group">
              <div class="d-block">
                <label for="initiative-area">Področje pobude*</label>
                <span v-if="errorInitiativeArea" class="error-message">Izberi področje pobude.</span>
              </div>
              <b-form-select
                id="initiative-area"
                v-model="initiativeArea"
                :class="{ 'form-control': true, 'error-input': errorInitiativeArea }"
                name="initiative-area"
                :options="initiativeAreaOptions"
                @blur="checkInitiativeArea"
              />
            </div>
            <div class="form-group">
              <label for="initiative-description">Opis*</label>
              <span v-if="errorInitiativeDescription" class="error-message">Vpiši opis pobude.</span>
              <textarea
                id="initiative-description"
                v-model.trim="initiativeDescription"
                :class="{ 'form-control': true, 'error-input': errorInitiativeDescription }"
                placeholder="Na katero težavo, pomanjkljivost, napako, okvaro, nevarnost se nanaša vaša pobuda?"
                rows="5"
                @blur="checkInitiativeDescription"
              />
            </div>
            <b-form-group class="mt-4">
              <b-form-textarea
                id="initiative-suggestion"
                v-model.trim="initiativeSuggestion"
                :class="{ 'form-control': true}"
                placeholder="Kakšen je vaš predlog rešitve, odprave pomanjkljivosti/slabosti?"
                rows="5"
              /> <!-- @change="checkInitiativeSuggestion" -->
            </b-form-group>
            <div class="form-group">
              <div class="d-block">
                <label for="initiative-location">Lokacija*</label>
                <span v-if="errorInitiativeLocation" class="error-message">Vpiši lokacijo pobude.</span>
              </div>
              <p class="form-note">
                Vpiši naslov ali povleci marker na lokacijo na zemljevidu.
              </p>
              <div class="d-inline-flex w-75 initiative-location-input">
                <input
                  id="initiative-location"
                  v-model.trim="initiativeLocation"
                  :class="{ 'form-control': true, 'error-input': errorInitiativeLocation }"
                  name="initiative-location"
                  type="text"
                  required
                  @blur="checkInitiativeLocation"
                >
                <b-button>POTRDI</b-button>
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
              <label>Naslovna slika*</label>
              <div
                :class="{'dropzone': true, 'drop-active': dropzone1Active}"
                @drop.prevent="dropHandler($event);"
                @dragover.prevent="dragOverHandler($event);"
                @dragenter.prevent=""
                @dragleave.prevent="dragLeaveHandler($event)"
              >
                <input
                  id="initiative-cover-image"
                  ref="inputField"
                  name="initiative-cover-image"
                  type="file"
                  class=""
                  required
                  accept="image/*"
                  style="display: none"
                  @change="processCoverImage"
                >
                <div class="d-flex align-items-center">
                  <label for="initiative-cover-image" class="drop-circle d-flex justify-content-center align-items-center">
                    <img src="~/assets/img/icons/add.png" alt="add">
                  </label>
                  <p :if="!coverImageFile">Dodaj sliko ali pa jih povleci in odloži. Dovoljeni formati so: gif, jpg, png. Velikost naj ne presega 5 MB.</p>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Datoteke</label>
              <div
                :class="{'dropzone': true, 'drop-active': dropzone2Active}"
                @drop.prevent="dropHandler($event);"
                @dragover.prevent="dragOverHandler($event);"
                @dragenter.prevent=""
                @dragleave.prevent="dragLeaveHandler($event)"
              >
                <input
                  id="initiative-files"
                  ref="inputField"
                  name="initiative-files"
                  type="file"
                  class=""
                  multiple
                  accept="image/*"
                  style="display: none"
                  @change="processFiles"
                >
                <div class="d-flex align-items-center">
                  <label for="initiative-files" class="drop-circle d-flex justify-content-center align-items-center">
                    <img src="~/assets/img/icons/add.png" alt="add">
                  </label>
                  <p>Dodaj datoteke ali pa jih povleci in odloži. Dovoljeni formati so: gif, jpg, png, doc, docx, pdf, odt.
                    Velikost naj ne presega 5 MB.</p>
                </div>
              </div>
            </div>
            <hr class="hr-upper">
            <hr class="hr-lower">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <b-button>Shrani</b-button>
                <b-button>Zavrzi</b-button>
              </div>
              <b-button>ODDAJ -></b-button>
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
      initiativeTitle: '',
      errorInitiativeTitle: false,
      initiativeArea: null,
      initiativeAreaOptions: [
        { value: null, text: 'Please select an option' },
        { value: 'a', text: 'This is First option' },
        { value: 'b', text: 'Selected Option' },
        { value: { C: '3PO' }, text: 'This is an option with object value' },
        { value: 'd', text: 'This one is disabled', disabled: true }
      ],
      errorInitiativeArea: false,
      initiativeDescription: '',
      errorInitiativeDescription: false,
      initiativeSuggestion: '',
      initiativeLocation: '',
      errorInitiativeLocation: false,
      initiativeLocationEmptyAllowed: false,
      coverImageFile: null,
      file2: null,
      dropzone1Active: false,
      dropzone2Active: false
    }
  },
  methods: {
    checkInitiativeTitle () {
      this.errorInitiativeTitle = this.initiativeTitle.length === 0
    },
    checkInitiativeArea () {
      console.log('error', this.initiativeArea.value === null)
      this.errorInitiativeArea = this.initiativeArea.value === null
    },
    checkInitiativeDescription () {
      this.errorInitiativeDescription = this.initiativeDescription.length === 0
    },
    checkInitiativeLocation () {
      if (!this.initiativeLocationEmptyAllowed) {
        this.errorInitiativeLocation = this.initiativeLocation.length === 0
      }
    },
    initiativeLocationEmpty () {
      if (this.initiativeLocationEmptyAllowed) {
        this.errorInitiativeLocation = false
      }
    },
    processCoverImage () {
      console.log('Processing')
    },
    processFiles () {
      console.log('Processing')
    },
    dropHandler (event) {
      console.log('Dropped')
      this.dropActive = false
    },
    dragOverHandler (event) {
      console.log('DragOver')
      this.dropActive = true
    },
    dragLeaveHandler (event) {
      console.log('Drag done')
      this.dropActive = false
    },
    createInitiative () {
      this.checkInitiativeTitle()
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

label {
  margin-top: 1.5rem;
}

hr {
  width: calc(100% + 3rem);
  margin-left: -1.5rem;
}

.form-subtitle {
  margin-bottom: 2rem;
  font-style: italic;
}

.error-message {
  font-size: 0.8rem;
  padding-left: 1rem;
}

.error-input {
  border: 1px solid #ab2131;
}

.initiative-location-input {
  button {
    margin: 0 1rem;
  }
}

</style>
