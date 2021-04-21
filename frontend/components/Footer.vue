<template>
  <b-container fluid>
    <b-row class="footer d-flex flex-column flex-md-row justify-content-between align-items-center">
      <NuxtLink to="/pogoji-uporabe" class="mb-3 mb-md-0">
        Pogoji uporabe
      </NuxtLink>
      <p class="footnote mb-0">
        Če imate kakršne koli težave pri vnosu pobude, nam to, prosim, sporočite na elektronski naslov <a href="mailto:im@maribor.si">im@maribor.si</a>.
        <br>
        Vašo težavo bomo poskusili rešiti v najkrajšem času.
      </p>
    </b-row>
    <b-row class="logos d-flex justify-content-center align-items-center">
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
  padding: 1.5rem 2rem;
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

  @media (min-width: 768px) {
    padding: 1rem 2rem;
  }

  .footnote {
    text-align: center;

    a {
      text-decoration: underline;
    }

    @media (min-width: 768px) {
      max-width: 50%;
      text-align: right;
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
