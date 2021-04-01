<template>
  <b-container fluid>
    <b-row class="footer d-flex justify-content-between align-items-center">
      <NuxtLink to="/pogoji-uporabe" class="">
        Pogoji uporabe
      </NuxtLink>
      <span class="footnote">
        Če imate kakršne koli težave pri vnosu pobude, nam to, prosim, sporočite na elektronski naslov <a href="mailto:im@maribor.si">im@maribor.si</a>.
        <br/>
        Vašo težavo bomo poskusili rešiti v najkrajšem času.
      </span>
    </b-row>
    <b-row class="logos d-flex justify-content-center align-items-center">
      <img src="~/assets/img/LOGO_COLOUR_RESILIENT.jpg" alt="" class="py-2">
      <img src="~/assets/img/Grb_novi_pisani.png" alt="" class="">
      <img src="~/assets/img/PRIZMA-SI-BEL.jpg" alt="" class="py-3">
    </b-row>
  </b-container>
</template>

<script>
export default {
}
</script>

<style scoped lang="scss">

.footer {
  padding: 1rem 2rem;
  background-color: #1a365d;
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;
  color: #f8f8f8;
  font-size: 0.8rem;

  a {
    color: #f8f8f8;

    &:hover {
      text-decoration: none;
      color: #ef7782;
    }
  }

  .footnote {
    max-width: 50%;
    text-align: right;

    a {
      text-decoration: underline;
    }
  }
}

.logos {
  background-color: white;

  img {
    max-height: 5rem;
  }
}

</style>
