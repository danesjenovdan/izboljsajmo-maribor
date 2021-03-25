<template>
  <b-container fluid class="mt-5">
    <b-row>
      <b-col cols="12" lg="4" class="position-relative">
        <div class="predlog-info mb-4 mb-lg-0">
          <div class="tags mb-2">
            <span class="pl-4">
              <span
                :class="{
                  'tag-mm': data.type === 'MM',
                  'tag-ii': data.type === 'II',
                  'tag-zm': data.type === 'ZM',
                }">
              </span>
              {{ $store.getters.initiativeTypes[data.type] }}
            </span>
            <span>{{ data.area.name }}</span>
          </div>
          <h1>{{ data.title }}</h1>
          <p class="posted">
            <span>{{ data.author }}</span>
            <span class="separator">|</span>
            <span>{{ date(data.created) }}</span>
          </p>
          <div v-if="data.location" class="address">
            <p>{{ data.address }}</p>
            <div id="map-wrap" class="mt-4">
              <client-only>
                <l-map
                  :zoom="13"
                  :min-zoom="11"
                  :center="[46.554650, 15.645881]"
                  :max-bounds="[
                    [46.46188844675249, 15.51583465730236],
                    [46.62102957408261, 15.783283325506178]
                  ]"
                >
                  <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png" />
                  <l-marker
                    :lat-lng="[data.location.coordinates[0], data.location.coordinates[1]]"
                    :icon="mapIcon"
                    @ready="setIconStyles"
                  />
                </l-map>
              </client-only>
            </div>
          </div>
          <hr>
          <b-row v-for="status in data.statuses" :key="status.status" class="status">
            <b-col cols="2" class="d-flex flex-column align-items-center">
              <div class="icon-circle d-flex justify-content-center align-items-center">
                <img :src="statusImage(status.status)" alt="status img">
              </div>
              <div class="line" />
            </b-col>
            <b-col class="pl-0">
              <div>
                <h6 class="text-uppercase">
                  {{ status.status }}
                </h6>
                <span>{{ date(status.created) }}</span>
                <p>{{ status.note }}</p>
              </div>
            </b-col>
          </b-row>
        </div>
      </b-col>
      <b-col cols="12" lg="8">
        <b-row>
          <b-col>
            <NuxtLink to="/predlogi" class="my-2 ml-lg-5 back">
              &lt;&lt; Nazaj na vse predloge
            </NuxtLink>
          </b-col>
        </b-row>
        <b-row>
          <b-col class="predlog-description mr-lg-5 p-lg-0">
            <b-row class="position-relative mb-5">
              <b-col>
                <div class="d-flex">
                  <img
                    v-if="data.cover_image"
                    :src="data.cover_image.image"
                    class="cover-image"
                    alt="Initiative cover image - before"
                  >
                  <img
                    v-if="data.cover_image_after"
                    :src="data.cover_image_after.image"
                    class="cover-image"
                    alt="Initiative cover image - after"
                  >
                </div>
                <b-button v-if="!data.has_voted" class="support-button" @click="vote">
                  <img src="~/assets/img/icons/love.svg" alt="heart">
                  <span>PODPRI</span>
                </b-button>
                <b-button v-if="data.has_voted" class="support-button" @click="removeVote">
                  <!--<img src="~/assets/img/icons/love.svg" alt="heart">-->
                  <span>GLAS ODDAN</span>
                </b-button>
              </b-col>
            </b-row>
            <b-row class="justify-content-center my-2">
              <b-col cols="12" lg="8">
                <p>
                  Vedno več bo deževnih dni (npr. petek) zima prihaja, Maribor pa vedno bolj mrtev. Mladih kolesarjev tudi v takšnih dneh ne bo, bodo pa ostareli, družine z otroci, dnevni migranti zaradi služb... Koroško cesto spreminjajo v enosmerno cesto, ampak s kolesarskimi stezami v obe smeri. Cesti brišejo črte po sredini in avtomobili se lahko srečajo le tako, da vozita oba delno po kolesarski stezi (slika 2 in 3). Na delu, kjer ni dovolj prostora, so pa enostavno prekinili kolesarsko stezo in jo premaknili na cestišče. V križišču z Ribiško (slika 5), kjer je bil prej varen dostop in vključitev na Koroško zaradi dodatno urejenega odcepa in kjer je res velik promet zaradi velikih parkirišč, ki so ga nasilno uničili s koščkom zelenice, so sedaj vrisana 3 mesta za taxi, a jih tu nikoli ni (slika 6) Taksisti so na Mlinski. V samem križišču sta vrisani kolesi, za zavijanje v levo in v desno. Zdaj pa čisto resno vprašanje: a niso kolesarji vozila na cestišču? Kako lahko kolo zavija na tem nepreglednem delu v levo, ko pa vendar mora vsako vozilo peljat v desno do rondoja, tam obrnit in se teh par metrov vrnit po desni strani cestišča. Še bolj resno vprašanje: dva dni imamo že kaos v Mariboru zaradi dodatnih semaforjev ob Dravi, mesto dobesedno stoji, gre za ljudi, ki ne živijo v samem centru in se ne morejo vozit s kolesi, deževnih dni bo vedno več in tudi zima... in kolesarske steze bodo prazne, ljudje ujeti v kaosu.
                </p>
              </b-col>
            </b-row>
            <b-row v-if="data.uploaded_files.length > 0" class="justify-content-center my-5">
              <b-col cols="12" lg="9">
                <div class="files">
                  <h6>Datoteke</h6>
                  <span v-for="file in data.uploaded_files" :key="file.id" class="mr-2">
                    {{ file.name }}
                  </span>
                  <div class="img-preview mt-4">
                    <a
                      v-for="file in data.uploaded_files"
                      :key="file.id"
                      :href="file.file"
                      class="mr-2"
                      download
                    >
                      <img
                        :src="file.file"
                        :alt="file.name"
                      >
                    </a>
                  </div>
                </div>
              </b-col>
            </b-row>
            <hr class="hr-upper">
            <hr class="hr-lower">
            <b-row class="justify-content-center mb-5">
              <b-col cols="12" lg="9">
                <CommentForm :id="id" />
                <div v-for="comment in data.comments" :key="comment.author + comment.created" class="comment">
                  <hr class="hr-upper">
                  <hr class="hr-lower">
                  <span>{{ comment.author }}</span>
                  <span class="separator">|</span>
                  <span>{{ date(comment.created ) }}</span>
                  <p>{{ comment.content }}</p>
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
import CommentForm from '~/components/forms/CommentForm'

export default {
  components: { CommentForm },
  asyncData ({ params, $axios, redirect }) {
    const id = params.id
    return $axios.get(`v1/initiatives/${id}`)
      .then((res) => {
        console.log(res.data)
        return { data: res.data, id }
      })
      .catch((e) => {
        return redirect('/404')
        // console.log(params)
      })
  },
  data () {
    return {
      id: '',
      data: {
      },
      mapIcon: null,
      errorVoted: false // za bodoci error message
    }
  },
  computed: {},
  methods: {
    setIconStyles () {
      this.mapIcon = this.$L.icon({
        iconUrl: require('@/assets/img/icons/pin.svg')
      })
    },
    date (date) {
      const d = new Date(date)
      return `${d.getDate()}.${d.getMonth() + 1}.${d.getFullYear()}` // months go 0-11
    },
    statusImage (s) {
      return require(`~/assets/img/icons/${s}.png`)
    },
    async vote () {
      const success = await this.$store.dispatch('postVote', {
        id: this.id
      })
      if (success) { // voted successfully
        this.data.has_voted = true
      } else { // error
        this.errorVoted = true
      }
    },
    async removeVote () {
      const success = await this.$store.dispatch('deleteVote', {
        id: this.id
      })
      if (success) { // unvoted successfully
        this.data.has_voted = false
      } else { // error
        this.errorVoted = true
      }
    }
  }
}
</script>

<style scoped lang="scss">

.predlog-info {
  background-color: #ab2131;
  color: white;
  padding: 2rem;
  z-index: 1;

  @media (min-width: 992px) {
    position: absolute;
    left: 2rem;
    right: -2rem;
  }

  .tags span {
    background-color: white;
    color: black;
    font-size: 0.75rem;
    padding: 0.4rem 0.8rem;
    margin-right: 0.75rem;
    border-radius: 1rem;
    position: relative;
    text-transform: lowercase;
    display: inline-block;

    &:first-letter {
      text-transform: capitalize;
    }

    span {
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
      position: absolute;
      height: 100%;
      padding: 0.5rem;
      left: 0;
      top: 0;

      &.tag-mm {
        background-color: #8cade2;
      }

      &.tag-ii {
        background-color: #70b6a3;
      }

      &.tag-zm {
        background-color: #d9ab27;
      }
    }
  }

  h1, h6 {
    font-weight: 700;
  }

  .posted {
    font-style: italic;
    font-weight: 600;

    .separator {
      margin: 0 0.5rem;
    }
  }

  .address {
    font-style: italic;
    font-weight: 600;

    p {
      margin-bottom: 0.5rem;
    }
  }

  #map-wrap {
    height: 15rem;
  }

  hr {
    border: 1px solid #71131e;
    margin: 1rem 0;
  }

  .status {
    h6 {
      margin-bottom: 0;
    }

    span, p {
      font-size: 0.75rem;
    }

    .icon-circle {
      background-color: #f4dde0;
      width: 2.5rem;
      height: 2.5rem;
      border-radius: 1.25rem;

      img {
        width: 70%;
        height: 70%;
      }
    }

    .line {
      background-color: #490b12;
      width: 3px;
      flex-grow: 1;
      margin: 0.3rem 0;
    }

    &:last-of-type {
      .line {
        display: none;
      }
    }
  }
}

.back {
  color: black;
  font-weight: 600;
  font-style: italic;
  display: block;

  &:hover {
    text-decoration: none;
    color: #ef7782;
  }
}

.predlog-description {
  margin-bottom: 3rem;
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;
  border-radius: 0.5rem;

  .cover-image {
    object-fit: cover;
    width: 100%;
    max-height: 25rem;
  }

  .support-button {
    margin: 0;
    padding: 0.75rem 1.5rem;
    position: absolute;
    right: 20%;
    bottom: -1.5rem;
    box-shadow: 2px 2px 5px #d3d7df;

    img {
      margin-right: 0.5rem;
    }
  }

  .files {
    border: 1px dashed #8cade2;
    border-radius: 15px;
    padding: 1rem;

    h6 {
      font-weight: 600;
      font-style: italic;
      margin-bottom: 12px;
    }

    span {
      font-size: 12px;
      background-color: #8cade2;
      border-radius: 12px;
      box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
      padding: 6px 12px;
    }

    .img-preview {
      img {
        object-fit: cover;
        height: 6rem;
        width: 6rem;
      }
    }
  }

  .comment {
    span {
      font-weight: 600;
      font-style: italic;
      font-size: 0.8rem;
    }

    .separator {
      margin: 0 0.25rem;
    }

    p {
      overflow-wrap: break-word;
      white-space: pre-wrap;
    }
  }
}

</style>
