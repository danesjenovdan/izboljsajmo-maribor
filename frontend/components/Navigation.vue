<template>
  <b-row>
    <b-navbar toggleable="md" class="navigation align-items-center justify-content-end">
      <b-navbar-toggle target="nav_collapse" class="d-flex align-items-center d-md-none">
        <MoreIcon />
      </b-navbar-toggle>
      <b-collapse id="nav_collapse" is-nav class="py-4 py-md-0">
        <b-navbar-nav class="ml-auto">
          <NuxtLink class="nav-link" to="/">
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
            to="/profil"
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
      this.$router.push('/profil')
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
  background-color: #1a365d;
  width: 100%;

  .navbar-nav .nav-link, .profile {
    text-align: center;
    color: white;
    font-size: 0.9rem;
    border-radius: 1.5rem;
    border: 1px solid #1a365d;
    margin-bottom: 0.25rem;
    padding: 0.25rem 0.75rem;

    @media (min-width: 768px) {
      text-align: left;
      margin-left: 1rem;
      // padding: 0.25rem 0.75rem;
      margin-bottom: 0;
    }

    &.login, &.profile {
      background-color: #ef7782;
      border-color: #ef7782;
      border-radius: 1.5rem;
      color: black;
    }

    &:hover {
      text-decoration: none;
      color: #1a365d;
      background-color: white;
      border-color: white;
      transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }
  }

  .navbar-nav .nuxt-link-exact-active {
    border: 1px solid white;

    &.profile {
      font-weight: 600;
      border-color: #ef7782;

      &:hover {
        border-color: white;
      }
    }
  }

  .navbar-toggler {
    border-color: white;
    // background-color: #ef7782;
    // border-color: #ef7782;
    border-radius: 1rem;
    padding: 0.3rem 0.6rem;

    svg {
      max-height: 1rem;
      max-width: 1rem;
      fill: white;
    }
  }

  .profileDropdown {
    position: absolute;
    right: 2rem;
    top: 170px;
    background-color: #f8f8f8;
    box-shadow: 0 0 5px #d4d9e1;
    border-radius: 0.5rem;
    z-index: 1000;

    @media (min-width: 576px) {
      box-shadow: 0 0 20px #d4d9e1;
      top: 60px;
    }

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
