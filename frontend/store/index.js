export const state = () => ({
  token: null,
  client_id: 'kIZWxeodL29mfaKSIGQWPUuuck8CXv3m58XuJ8Y7',
  client_secret: '54pWmrpj1y9FiwkUDofjeP4B5tbLQ4wW6F2wqsMT3JuQN4ApIqcveKlzOC1laQIJp8JpVi99EheHCkumEJ0o81J9f2uHK3eXjUdxprzDnWlsTuZM6cgv1Eo35KSr7Mfg',
  grant_type: 'password'
})

export const getters = {
  token (state) {
    return state.token
  },
  client_id (state) {
    return state.client_id
  },
  client_secret (state) {
    return state.client_secret
  },
  grant_type (state) {
    return state.grant_type
  },
  isAuthenticated (state) {
    return !!state.token
  }
}

export const mutations = {
  setToken (state, payload) {
    state.token = payload.token
  }
}

export const actions = {
  async login (context, payload) {
    const loginData = {
      username: payload.form.username,
      password: payload.form.password,
      client_id: context.getters.client_id,
      client_secret: context.getters.client_secret,
      grant_type: context.getters.grant_type
    }
    // console.log(loginData)
    const response = await this.$axios.post('auth/token/', loginData)
    const responseData = await response.data

    if (response.status === 200) {
      context.commit('setToken', { token: responseData.access_token })
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  },
  logout (context) {
    // context.commit('setAuth', { isAuth: false })
  },
  async register (context, payload) {
    const registerData = {
      username: payload.form.username,
      email: payload.form.email,
      password: payload.form.password,
      phone_number: payload.form.phone
    }
    console.log(registerData)
    const response = await this.$axios.post('v1/users/', registerData)
    const responseData = await response.data

    if (response.status === 200) {
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  },
  async registerOrganization (context, payload) {
    const registerData = {
      organization_name: payload.form.username,
      username: payload.form.name,
      email: payload.form.email,
      password: payload.form.password,
      phone_number: payload.form.phone,
      number_of_members: payload.form.membersNumber
    }
    // console.log(registerData)
    const response = await this.$axios.post('v1/organizations/', registerData)
    const responseData = await response.data

    if (response.status === 200) {
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  },
  async postComment (context, payload) {
    const newComment = {
      content: payload.content
    }
    const response = await this.$axios.post(`v1/initiatives/${payload.id}/comments/`, newComment)
    const responseData = await response.data

    if (response.status === 200) {
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  },
  async postInitiative (context, payload) {
    const response = await this.$axios.post('v1/initiatives/', payload)
    const responseData = await response.data

    if (response.status === 200) {
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  }
}
