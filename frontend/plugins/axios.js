import createAuthRefreshInterceptor from 'axios-auth-refresh'

export default function ({ $axios, store }) {
  const instance = $axios.create()
  delete instance.defaults.headers.common.Authorization
  // Function that will be called to refresh authorization
  const refreshAuthLogic = failedRequest => instance.post('auth/token/', {
    refresh_token: store.$auth.strategy.refreshToken.get(),
    client_id: store.state.client_id,
    client_secret: store.state.client_secret,
    grant_type: 'refresh_token'
  })
    .then((tokenRefreshResponse) => {
      store.$auth.setUserToken(tokenRefreshResponse.data.access_token, tokenRefreshResponse.data.refresh_token).then(() => {
        failedRequest.response.config.headers.Authorization = 'Bearer ' + tokenRefreshResponse.data.token
        return Promise.resolve()
      })
    }).catch(() => {
      store.$auth.logout()
    })

  // by default intercepts 401
  createAuthRefreshInterceptor(
    $axios,
    refreshAuthLogic,
    {
      pauseInstanceWhileRefreshing: true
    }
  )
}
