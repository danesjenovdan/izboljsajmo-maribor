<template>
  <b-container>
    <b-row class="my-5">
      <b-col>
        <div
          v-for="(el, index) in data"
          :key="index"
        >
          <h1 v-if="el.type === 'H2'">
            {{ el.content }}
          </h1>
          <h2 v-if="el.type === 'H3'">
            {{ el.content }}
          </h2>
          <p v-if="el.type === 'TXT'">
            {{ el.content }}
          </p>
          <img
            v-if="el.type === 'IMG'"
            alt="O Izboljšajmo Maribor"
            :src="el.url || el.image"
            class="img-fluid"
          >
          <div
            v-if="el.type === 'YT'"
            class="embed-responsive embed-responsive-16by9 video"
          >
            <iframe class="embed-responsive-item p-4" :src="youtubeEmbedLink(el.url)" allowfullscreen />
          </div>
          <div
            v-if="el.type === 'LINK'"
            class="about-link"
          >
            <a :href="el.url" target="_blank">{{ el.content }}</a>
          </div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  asyncData ({ $axios, redirect }) {
    return $axios.get('v1/about')
      .then((res) => {
        return { data: res.data }
      })
      .catch((e) => {
        // return redirect('/404')
        // console.log(e)
      })
  },
  methods: {
    youtubeEmbedLink (url) {
      const id = url.split('?v=')[1]
      return 'https://www.youtube.com/embed/' + id
    }
  }
}
</script>

<style scoped lang="scss">

p {
  font-size: 1.25rem;
  font-weight: 300;
  line-height: 1.5;
}

h1, h2 {
  margin-bottom: 1.5rem;
  font-weight: 700;
}

h2 {
  margin-top: 1.5rem;
}

img, .video {
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.about-link {
  margin-bottom: 0.25rem;
}

.about-link a {
  font-size: 20px;
  font-weight: 500;
  color: #ef7782;
}

</style>
