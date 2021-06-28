export default function ({ redirect, $axios, store }) {
  $axios.onError((error) => {
    const code = parseInt(error.response && error.response.status)
    if (code === 401) {
      store.$auth.strategy.token.reset()
      $axios.post('auth/token/', {
        refresh_token: store.$auth.strategy.refreshToken.get(),
        client_id: store.state.client_id,
        client_secret: store.state.client_secret,
        grant_type: 'refresh_token'
      }).then((response) => {
        store.$auth.setUserToken(response.data.access_token, response.data.refresh_token).then(() => {
          store.$router.go()
        })
      }).catch(() => {
        store.$auth.logout()
      })
    }
  })
}
