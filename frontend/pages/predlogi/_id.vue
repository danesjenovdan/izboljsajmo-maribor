<template>
  <b-container fluid class="my-5">
    <b-row>
      <b-col cols="12" lg="4">
        <div class="predlog-info position-relative mb-4 mb-lg-0">
          <div class="tags mb-2">
            <span class="pl-4">
              <span
                :class="{
                  'tag-mm': data.type === 'MM',
                  'tag-ii': data.type === 'II',
                  'tag-zm': data.type === 'ZM',
                }"
              />
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
                    :lat-lng="[data.location.coordinates[1], data.location.coordinates[0]]"
                    :icon="mapIcon"
                    @ready="setIconStyles"
                  />
                </l-map>
              </client-only>
            </div>
          </div>
          <div v-if="!data.location" class="font-italic">
            Predlog nima lokacije.
          </div>
          <hr>
          <b-row
            v-for="status in data.statuses"
            :key="status.status"
            class="status"
          >
            <b-col cols="2" class="d-flex flex-column align-items-center">
              <div class="icon-circle d-flex justify-content-center align-items-center">
                <img v-if="status.responses" :src="statusImage(status.responses[0].status)" alt="status img">
              </div>
              <div class="line" />
            </b-col>
            <b-col class="pl-0">
              <div>
                <h6 class="text-uppercase">
                  {{ status.status }}
                </h6>
                <div v-for="response in status.responses" :key="response.created">
                  <span>{{ date(response.created) }}</span>
                  <p>{{ response.note }}</p>
                </div>
              </div>
            </b-col>
          </b-row>
        </div>
      </b-col>
      <b-col cols="12" lg="8">
        <b-row>
          <b-col>
            <NuxtLink to="/" class="my-2 ml-lg-5 back">
              &lt;&lt; Nazaj na vse predloge
            </NuxtLink>
          </b-col>
        </b-row>
        <b-row class="pr-lg-4">
          <b-col class="predlog-description">
            <b-row class="position-relative" :class="{ 'mb-5': data.cover_image || data.cover_image_after }">
              <b-col class="p-lg-0" :class="{ 'd-flex justify-content-end': !(data.cover_image || data.cover_image_after) }">
                <div class="d-flex flex-column flex-md-row position-relative">
                  <span v-if="data.cover_image" class="image-label image-label-before">Prej</span>
                  <img
                    v-if="data.cover_image"
                    :src="data.cover_image.image"
                    class="cover-image"
                    :class="{
                      'stretch-image': !data.cover_image_after
                    }"
                    alt="Initiative cover image - before"
                  >
                  <span v-if="data.cover_image_after" class="image-label image-label-after">Potem</span>
                  <img
                    v-if="data.cover_image_after"
                    :src="data.cover_image_after.image"
                    class="cover-image"
                    alt="Initiative cover image - after"
                  >
                </div>
                <b-button
                  v-if="!data.has_voted"
                  class="support-button"
                  :class="{
                    'button-reposition': !(data.cover_image || data.cover_image_after)
                  }"
                  @click="vote"
                >
                  <LikeIcon />
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
                <div
                  v-for="description in data.descriptions"
                  :key="description.order"
                >
                  <h6>{{ description.title }}</h6>
                  <p>{{ description.content }}</p>
                </div>
              </b-col>
            </b-row>
            <b-row v-if="data.uploaded_files.length > 0" class="justify-content-center my-5">
              <b-col cols="12" lg="9">
                <div class="files">
                  <h6>Datoteke</h6>
                  <a
                    v-for="file in data.uploaded_files"
                    :key="file.id"
                    :href="file.file"
                    target="_blank"
                    download
                  >
                    <span class="mr-2 mb-1 d-inline-block">
                      {{ file.name }}
                    </span>
                  </a>
                  <div class="img-preview mt-4">
                    <a
                      v-for="file in uploaded_images"
                      :key="file.id"
                      :href="file.file"
                      target="_blank"
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
import LikeIcon from '~/assets/img/icons/like.svg?inline'

export default {
  components: { CommentForm, LikeIcon },
  asyncData ({ params, $axios, redirect }) {
    const id = params.id
    return $axios.get(`v1/initiatives/${id}`)
      .then((res) => {
        return { data: res.data, id }
      })
      .catch((e) => {
        // return redirect('/predlogi')
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
  computed: {
    uploaded_images () {
      return this.data.uploaded_files.filter(file => file.file.split('.').pop().toLowerCase() === 'jpg' || file.file.split('.').pop().toLowerCase() === 'jpeg' || file.file.split('.').pop().toLowerCase() === 'png')
    }
  },
  methods: {
    setIconStyles () {
      this.mapIcon = this.$L.icon({
        iconUrl: require('@/assets/img/icons/pin.svg'),
        iconSize: [32, 32]
      })
    },
    date (date) {
      const d = new Date(date)
      return `${d.getDate()}. ${d.getMonth() + 1}. ${d.getFullYear()}` // months go 0-11
    },
    statusImage (s) {
      try {
        return require(`~/assets/img/icons/statuses/${s}.svg`)
      } catch (e) {
        return ''
      }
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
  padding: 1rem;
  z-index: 1;

  @media (min-width: 992px) {
    padding: 2rem 0 2rem 2rem;

    &:after {
      content: "";
      background-color: #ab2131;
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      right: -2rem;
      z-index: -1;
    }
  }

  .tags span {
    background-color: white;
    color: black;
    font-size: 0.75rem;
    padding: 0.25rem 0.8rem;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
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
    // width: 100%;
    height: 14rem;
    min-width: 50%;

    @media (min-width: 576px) {
      max-height: 25rem;
      height: unset;
    }

    &.stretch-image {
      min-width: 100%;
    }
  }

  .image-label {
    position: absolute;
    top: 1rem;
    padding: 0.125rem 0.75rem;
    border: 1px solid #ffffff;
    border-radius: 18px;
    background-color: #e8ebef;
    text-transform: uppercase;
    font-weight: 500;
    font-size: 0.75rem;

    &.image-label-before {
      left: 1rem;
    }

    &.image-label-after {
      top: calc(50% + 1rem);
      left: 1rem;
    }

    @media (min-width: 576px) {
      &.image-label-after {
        top: 1rem;
        left: calc(50% + 1rem);
      }
    }

    @media (min-width: 992px) {
      top: unset;
      bottom: 1rem;
      padding: 0.25rem 1rem;
      // font-size: 1rem;

      &.image-label-before {
        left: 2rem;
      }

      &.image-label-after {
        top: unset;
        left: calc(50% + 1rem);
      }
    }
  }

  .support-button {
    margin: 0;
    padding: 0.75rem 1.5rem;
    position: absolute;
    right: 20%;
    bottom: -1.5rem;
    box-shadow: 2px 2px 5px #d3d7df;

    &.button-reposition {
      position: relative;
      right: unset;
      bottom: unset;
      margin-bottom: 1rem;
    }
    @media (min-width: 992px) {
      &.button-reposition {
        right: calc(12.5% + 15px);
        bottom: 2rem;
        margin-bottom: 0;
      }
    }

    img {
      margin-right: 0.5rem;
    }
  }

  .files {
    border: 1px dashed #8cade2;
    border-radius: 15px;
    padding: 1rem;

    a {
      text-decoration: none;
      color: black;
    }

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
