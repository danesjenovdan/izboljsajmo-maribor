export const state = () => ({
  client_id: 'kIZWxeodL29mfaKSIGQWPUuuck8CXv3m58XuJ8Y7',
  client_secret: '54pWmrpj1y9FiwkUDofjeP4B5tbLQ4wW6F2wqsMT3JuQN4ApIqcveKlzOC1laQIJp8JpVi99EheHCkumEJ0o81J9f2uHK3eXjUdxprzDnWlsTuZM6cgv1Eo35KSr7Mfg',
  grant_type: 'password',
  initiativeTypes: {
    MM: 'MOTI ME!',
    II: 'IMAM IDEJO!',
    ZM: 'ZANIMA ME!'
  }
})

export const getters = {
  token (state) {
    // console.log('getting', window.localStorage.getItem('authToken'))
    // return window.localStorage.getItem('authToken')
    return window.localStorage.getItem('authToken')
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
    // console.log('isAuthenticated', window.localStorage.getItem('authToken'))
    return !!window.localStorage.getItem('authToken')
  },
  initiativeTypes (state) {
    return state.initiativeTypes
  }
}

export const mutations = {
  setToken (state, payload) {
    window.localStorage.setItem('authToken', payload.token)
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
    context.commit('setToken', { token: '' })
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
    const response = await this.$axios.post(`v1/initiatives/${payload.id}/comments/`, newComment, {
      headers: { Authorization: 'Bearer ' + context.getters.token }
    })
    const responseData = await response.data

    if (response.status === 201) {
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  },
  async postCoverImage (context, payload) {
    const formData = new FormData()
    formData.append('image', payload.image)
    const response = await this.$axios.post('v1/images/', formData, {
      headers: {
        Authorization: 'Bearer ' + context.getters.token,
        'Content-Type': 'multipart/form-data'
      }
    })
    const responseData = await response.data
    console.log(response)

    if (response.status === 201) { // Created
      return responseData.id
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  },
  async postFiles (context, payload) {
    const formData = new FormData()
    formData.append('file', payload.file)
    formData.append('name', payload.name)
    const response = await this.$axios.post('v1/files/', formData, {
      headers: {
        Authorization: 'Bearer ' + context.getters.token,
        'Content-Type': 'multipart/form-data'
      }
    })
    const responseData = await response.data
    console.log(response)

    if (response.status === 201) { // Created
      return responseData.id
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  },
  async postInitiative (context, payload) {
    const form = {
      title: payload.initiativeTitle,
      type: 'II',
      area: payload.initiativeArea,
      address: 'Županova',
      location: payload.initiativeLocation,
      descriptions: [
        {
          title: 'To je nek title',
          field: 'to_bo_nek_kljuc',
          content: payload.initiativeDescription
        },
        {
          title: 'To je nek title 2',
          field: 'to_bo_nek_kljuc 2',
          content: payload.initiativeSuggestion
        }
      ],
      cover_image: payload.initiativeCoverImage,
      uploaded_files: payload.initiativeFiles
    }
    console.log(JSON.stringify(form))
    const response = await this.$axios.post('v1/initiatives/', form, {
      headers: {
        Authorization: 'Bearer ' + context.getters.token
      }
    })
    const responseData = await response.data

    if (response.status === 201) {
      console.log(responseData)
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  }
}
