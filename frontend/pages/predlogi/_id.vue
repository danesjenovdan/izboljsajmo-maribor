<template>
  <b-container fluid class="mt-5">
    <b-row>
      <b-col cols="4" class="position-relative">
        <div class="predlog-info">
          <div class="tags mb-2">
            <span>
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
          <div class="address">
            <p>{{ data.address }}</p>
            <!-- TO DO: insert real map -->
            <img src="~/static/map.png" class="map img-fluid">
          </div>
          <hr>
          <b-row v-for="status in data.statuses" :key="status.status" class="status">
            <b-col cols="2" class="d-flex flex-column align-items-center">
              <div class="icon-circle d-flex justify-content-center align-items-center">
                <img :src="statusImage(status.status)" alt="status img">
              </div>
              <div class="line"></div>
            </b-col>
            <b-col class="pl-0">
              <div>
                <h6 class="text-uppercase">{{ status.status }}</h6>
                <span>{{ date(status.created) }}</span>
                <p>{{ status.note }}</p>
              </div>
            </b-col>
          </b-row>
        </div>
      </b-col>
      <b-col cols="8">
        <b-row>
          <NuxtLink to="/predlogi" class="my-2 back">
            &lt;&lt; Nazaj na vse predloge
          </NuxtLink>
        </b-row>
        <b-row>
          <b-col class="predlog-description p-0">
            <b-row class="position-relative mb-5">
              <b-col>
                <img :src="data.cover_image.image" class="cover-image img-fluid" alt="Initiative cover image">
                <b-button class="support-button">
                  <img src="~/assets/img/icons/love.png" alt="heart">
                  PODPRI
                </b-button>
              </b-col>
            </b-row>
            <b-row class="justify-content-center my-2">
              <b-col cols="8">
                <p>
                  Vedno več bo deževnih dni (npr. petek) zima prihaja, Maribor pa vedno bolj mrtev. Mladih kolesarjev tudi v takšnih dneh ne bo, bodo pa ostareli, družine z otroci, dnevni migranti zaradi služb... Koroško cesto spreminjajo v enosmerno cesto, ampak s kolesarskimi stezami v obe smeri. Cesti brišejo črte po sredini in avtomobili se lahko srečajo le tako, da vozita oba delno po kolesarski stezi (slika 2 in 3). Na delu, kjer ni dovolj prostora, so pa enostavno prekinili kolesarsko stezo in jo premaknili na cestišče. V križišču z Ribiško (slika 5), kjer je bil prej varen dostop in vključitev na Koroško zaradi dodatno urejenega odcepa in kjer je res velik promet zaradi velikih parkirišč, ki so ga nasilno uničili s koščkom zelenice, so sedaj vrisana 3 mesta za taxi, a jih tu nikoli ni (slika 6) Taksisti so na Mlinski. V samem križišču sta vrisani kolesi, za zavijanje v levo in v desno. Zdaj pa čisto resno vprašanje: a niso kolesarji vozila na cestišču? Kako lahko kolo zavija na tem nepreglednem delu v levo, ko pa vendar mora vsako vozilo peljat v desno do rondoja, tam obrnit in se teh par metrov vrnit po desni strani cestišča. Še bolj resno vprašanje: dva dni imamo že kaos v Mariboru zaradi dodatnih semaforjev ob Dravi, mesto dobesedno stoji, gre za ljudi, ki ne živijo v samem centru in se ne morejo vozit s kolesi, deževnih dni bo vedno več in tudi zima... in kolesarske steze bodo prazne, ljudje ujeti v kaosu.
                </p>
              </b-col>
            </b-row>
            <b-row class="justify-content-center my-5">
              <b-col cols="9">
                <div class="files">
                  <h6>Datoteke</h6>
                  <span v-for="file in data.uploaded_files" :key="file.id" class="mr-2">
                    {{ file.name }}
                  </span>
                  <div class="img-preview mt-4">
                    <img v-for="file in data.uploaded_files" :key="file.id" :src="file.file" :alt="file.name" class="mr-2">
                  </div>
                </div>
              </b-col>
            </b-row>
            <hr class="hr-upper">
            <hr class="hr-lower">
            <b-row class="justify-content-center mb-5">
              <b-col cols="9">
                <CommentForm :id="id" />
                <div v-for="comment in data.comments" :key="comment.author" class="comment">
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
export default {
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
        area: '',
        type: '',
        title: '',
        author: '',
        created: ''
      }
    }
  },
  computed: {},
  methods: {
    date (date) {
      const d = new Date(date)
      return `${d.getDate()}.${d.getMonth() + 1}.${d.getFullYear()}` // months go 0-11
    },
    statusImage (s) {
      return require(`~/assets/img/icons/${s}.png`)
    }
  }
}
</script>

<style scoped lang="scss">

.predlog-info {
  background-color: #ab2131;
  color: white;
  padding: 2rem;
  position: absolute;
  left: 2rem;
  right: -2rem;
  z-index: 1;

  .tags span {
    background-color: white;
    color: black;
    font-size: 0.75rem;
    padding: 0.4rem 0.8rem;
    margin-right: 0.4rem;
    border-radius: 1rem;
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
  margin-left: 3rem;

  &:hover {
    text-decoration: none;
    color: #ef7782;
  }
}

.predlog-description {
  margin-right: 3rem;
  margin-bottom: 3rem;
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;
  border-radius: 0.5rem;

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
        max-height: 100px;
        max-width: 100px;
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
  }
}

</style>
