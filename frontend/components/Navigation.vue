<template>
  <b-container fluid>
    <b-row>
      <b-navbar toggleable="md" class="navigation align-items-center">
        <NuxtLink to="/predlogi">
          <img src="~/assets/img/izboljsajmo_maribor_logo.png" alt="">
        </NuxtLink>
        <b-navbar-toggle target="nav_collapse">
          <img src="~/assets/img/icons/more.png" alt="toggle menu">
        </b-navbar-toggle>
        <b-collapse is-nav id="nav_collapse" class="py-4 py-md-0">
          <b-navbar-nav class="ml-auto">
            <NuxtLink v-if="!isAuthenticated" class="nav-link" to="/predlogi">
              Domov
            </NuxtLink>
            <NuxtLink v-if="isAuthenticated" class="nav-link" to="/predlogi" @click.prevent="">
              Vsi predlogi
            </NuxtLink>
            <NuxtLink v-if="!isAuthenticated" class="nav-link" to="/o-izboljsajmo-maribor">
              O izboljšajmo Maribor
            </NuxtLink>
            <NuxtLink class="nav-link" to="/pomoc">
              Pomoč
            </NuxtLink>
            <NuxtLink v-if="!isAuthenticated" class="login nav-link" to="/prijava">
              Prijava
            </NuxtLink>
            <NuxtLink
              v-if="isAuthenticated"
              class="profile nav-link"
              to="/"
              event=""
              @click.native="showProfileDropdown = !showProfileDropdown"
            >
              <!-- event="" is to disable the link -->
              Moj profil
            </NuxtLink>
            <div v-if="showProfileDropdown" class="profileDropdown">
              <h3 class="pt-4 text-center font-weight-bold">
                {{ this.$auth.user.username }}
              </h3>
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
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
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
  width: 100%;

  img {
    height: 40px;
  }

  .navbar-nav .nav-link {
    text-align: center;
    color: #606060;
    font-size: 0.8rem;
    border-radius: 1.5rem;
    border: 2px solid #f8f8f8;
    margin-bottom: 0.25rem;

    @media (min-width: 768px) {
      text-align: left;
      margin-left: 1rem;
      padding: 0.25rem 0.75rem;
    }

    &.nuxt-link-exact-active {
      border: 2px solid #a92332;
    }

    &.profile.nuxt-link-exact-active {
      font-weight: 600;
    }

    &.login {
      background-color: rgba(239, 119, 130, 0.3);
      border-radius: 1.5rem;
    }

    &:hover {
      text-decoration: none;
      color: #a92332;
    }

    &.profile {
      background-color: #ef7782;
      border-color: #ef7782;
      box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
      color: black;

      &:hover {
        background-color: #6c757d;
        border-color: #6c757d;
        color: white;
        transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
      }
    }
  }

  .navbar-toggler {
    img {
      height: 1rem;
    }
  }

  .profileDropdown {
    position: absolute;
    right: 2rem;
    top: calc(3rem + 40px);
    background-color: #f8f8f8;
    box-shadow: 0 0 20px #d4d9e1;
    border-radius: 0.5rem;
    z-index: 1000;

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
