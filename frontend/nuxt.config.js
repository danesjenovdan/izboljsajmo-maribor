export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'izboljsajmo-maribor',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700&display=swap' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/assets/css/main.scss'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    'bootstrap-vue/nuxt',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://auth.nuxtjs.org/
    '@nuxtjs/auth-next',
    'nuxt-leaflet'
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    baseURL: 'https://api.izboljsajmo-maribor.k8s.djnd.si' // TODO
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  },

  router: {
  },

  auth: {
    strategies: {
      local: {
        token: {
          property: 'access_token',
          required: true,
          name: 'Authorization',
          type: 'Bearer'
        },
        endpoints: {
          login: { url: '/auth/token', method: 'post' },
          user: false,
          logout: false
        },
        clientId: 'kIZWxeodL29mfaKSIGQWPUuuck8CXv3m58XuJ8Y7',
        grantType: 'password'
      }
      /*
      social: {
        scheme: 'oauth2',
        endpoints: {
          authorization: 'http://localhost:8000/auth/token/',
          token: false,
          logout: 'https://example.com/logout'
        },
        grantType: 'password',
        redirectUri: '/login',
        logoutRedirectUri: '/predlogi',
        clientId: 'kIZWxeodL29mfaKSIGQWPUuuck8CXv3m58XuJ8Y7',
        scope: ['openid', 'profile', 'email'],
        autoLogout: false
      }
      */
    },
    redirect: {
      login: '/prijava',
      logout: '/predlogi',
      home: '/'
    }
  },
  server: {
    port: 3000, // default: 3000
    host: '0.0.0.0', // default: localhost,
    timing: false
  }
}
