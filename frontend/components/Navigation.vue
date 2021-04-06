<template>
  <b-container fluid>
    <b-row>
      <b-navbar toggleable="md" class="navigation align-items-center">
        <NuxtLink to="/predlogi">
          <img src="~/assets/img/izboljsajmo_maribor_logo.png" alt="Izboljšajmo Maribor LOGO">
        </NuxtLink>
        <b-navbar-toggle target="nav_collapse">
          <MoreIcon />
        </b-navbar-toggle>
        <b-collapse id="nav_collapse" is-nav class="py-4 py-md-0">
          <b-navbar-nav class="ml-auto">
            <NuxtLink class="nav-link" to="/predlogi">
              Vsi predlogi
            </NuxtLink>
            <NuxtLink class="nav-link" to="/o-izboljsajmo-maribor">
              O Izboljšajmo Maribor
            </NuxtLink>
            <NuxtLink v-if="!isAuthenticated" class="login nav-link" to="/prijava">
              Prijava
            </NuxtLink>
            <NuxtLink
              v-if="isAuthenticated"
              id="profile-button"
              class="profile"
              to="/"
              event=""
              @click.native="toggleDropdown"
            >
              <!-- event="" is to disable the link -->
              Moj profil
            </NuxtLink>
            <div v-if="showProfileDropdown" v-click-outside="closeProfileDropdown" class="profileDropdown">
              <h3 class="pt-4 text-center font-weight-bold">
                {{ this.$auth.user.username }}
              </h3>
              <hr class="hr-upper">
              <hr class="hr-lower">
              <div class="text-center">
                <b-button
                  class="nav-link my-initiatives-button w-75 position-relative d-inline-flex justify-content-center align-items-center"
                  @click="myInitiatives"
                >
                  MOJI PREDLOGI
                  <ArrowRightIcon class="position-absolute" />
                </b-button>
                <b-button
                  class="logout-button w-75 position-relative d-inline-flex justify-content-center align-items-center"
                  @click="logout"
                >
                  ODJAVA
                  <ExitRightIcon class="position-absolute" />
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
import MoreIcon from '~/assets/img/icons/more.svg?inline'
import ArrowRightIcon from '~/assets/img/icons/arrow-right.svg?inline'
import ExitRightIcon from '~/assets/img/icons/exit-right.svg?inline'

export default {
  components: { MoreIcon, ArrowRightIcon, ExitRightIcon },
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
    },
    closeProfileDropdown (e) {
      if (e.target.id !== 'profile-button') {
        this.showProfileDropdown = false
      }
    },
    toggleDropdown () {
      this.showProfileDropdown = !this.showProfileDropdown
    }
  }
}
</script>

<style scoped lang="scss">

.navigation {
  padding: 0.5rem 2rem;
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;
  background-color: #f8f8f8;
  width: 100%;

  img {
    height: 50px;
  }

  .navbar-nav .nav-link, .profile {
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

    &.login {
      background-color: rgba(239, 119, 130, 0.3);
      border-radius: 1.5rem;
    }

    &:hover {
      text-decoration: none;
      color: #a92332;
    }
  }

  .navbar-nav .nav-link.nuxt-link-exact-active {
    border: 2px solid #a92332;
  }

  .profile {
    background-color: #ef7782;
    border-color: #ef7782;
    box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
    color: black;
    padding: 0.25rem 0.75rem;

    &:hover {
      text-decoration: none;
      background-color: #1A365D;
      border-color: #1A365D;
      color: white;
      transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }

    &.nuxt-link-exact-active {
      font-weight: 600;
    }
  }

  .navbar-toggler {
    svg {
      max-height: 1rem;
      max-width: 1rem;
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
      margin: 0 0 1.5rem 0;
      padding: 0.4rem 2rem 0.4rem 0.75rem;
      font-size: 1rem;
      border: none;
      color: black;

      &:hover {
        background-color: #1A365D;
        border-color: #1A365D;
        color: white;
      }
    }
  }
}

</style>
