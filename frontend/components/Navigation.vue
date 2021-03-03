<template>
  <b-container fluid>
    <b-row class="navigation justify-content-between align-items-center">
      <img src="~/assets/img/izboljsajmo_maribor_logo.png" alt="">
      <div class="">
        <NuxtLink v-if="!isAuthenticated" to="/predlogi">
          Domov
        </NuxtLink>
        <NuxtLink v-if="!isAuthenticated" to="/o-izboljsajmo-maribor">
          O izboljšajmo Maribor
        </NuxtLink>
        <NuxtLink v-if="!isAuthenticated" to="/pomoc">
          Pomoč
        </NuxtLink>
        <NuxtLink v-if="!isAuthenticated" class="login" to="/prijava">
          Prijava
        </NuxtLink>
        <NuxtLink v-if="isAuthenticated" class="" to="/predlogi/nov" @click.prevent="">
          Imam predlog
        </NuxtLink>
        <NuxtLink v-if="isAuthenticated" class="" to="/predlogi" @click.prevent="">
          Vsi predlogi
        </NuxtLink>
        <NuxtLink v-if="isAuthenticated" class="profile" to="" @click.native="showProfileDropdown = !showProfileDropdown">
          Moj profil
        </NuxtLink>
        <div v-if="showProfileDropdown" class="profileDropdown">
          <h3 class="pt-4 text-center font-weight-bold">Janez Novak</h3>
          <hr class="hr-upper">
          <hr class="hr-lower">
          <div class="text-center">
            <b-button
              class="my-initiatives-button w-75 position-relative d-inline-flex justify-content-center"
              @click="myInitiatives"
            >
              MOJI PREDLOGI
              <img src="~/assets/img/icons/arrow-right.png" alt="logout icon" class="position-absolute">
            </b-button>
            <b-button
              class="logout-button w-75 position-relative d-inline-flex justify-content-center"
              @click="logout"
            >
              ODJAVA
              <img src="~/assets/img/icons/exit-right.png" alt="logout icon" class="position-absolute">
            </b-button>
          </div>
        </div>
      </div>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data () {
    return {
      showProfileDropdown: false
    }
  },
  computed: {
    isAuthenticated () {
      return this.$auth.loggedIn
    }
  },
  methods: {
    myInitiatives () {
      this.showProfileDropdown = !this.showProfileDropdown
      this.$router.push('/')
    },
    async logout () {
      this.showProfileDropdown = !this.showProfileDropdown
      await this.$store.dispatch('logout')
    }
  }
}
</script>

<style scoped lang="scss">

.navigation {
  padding: 1rem 2rem;
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;
  background-color: #f8f8f8;

  img {
    height: 40px;
  }

  a {
    color: #606060;
    margin-left: 1rem;
    padding: 0.5rem 1rem;

    &:hover {
      text-decoration: none;
      color: #ef7782;
    }

    &.login {
      background-color: rgba(239, 119, 130, 0.3);
      border-radius: 1.5rem;
    }

    &.profile {
      background-color: #ef7782;
      box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
      border-radius: 1.5rem;
      font-weight: 600;
      color: black;

      &:hover {
        background-color: #6c757d;
        color: white;
        transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
      }
    }
  }

  .profileDropdown {
    position: absolute;
    right: 2rem;
    top: calc(3rem + 40px);
    background-color: #f8f8f8;
    box-shadow: 0 0 20px #d4d9e1;
    border-radius: 0.5rem;
    z-index: 1;

    .logout-button {
      background-color: #d7d7d7;
    }

    .logout-button, .my-initiatives-button {
      margin-top: 0;
      margin-bottom: 1.5rem;
      padding-right: 2rem;

      &:hover {
        background-color: #6c757d;
      }

      img {
        right: 0.5rem;
        height: 1.5rem;
      }
    }
  }
}

</style>
