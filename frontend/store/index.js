export const state = () => ({
  client_secret: '54pWmrpj1y9FiwkUDofjeP4B5tbLQ4wW6F2wqsMT3JuQN4ApIqcveKlzOC1laQIJp8JpVi99EheHCkumEJ0o81J9f2uHK3eXjUdxprzDnWlsTuZM6cgv1Eo35KSr7Mfg',
  user: null,
  initiativeTypes: {
    MM: 'MOTI ME!',
    II: 'IMAM IDEJO!',
    ZM: 'ZANIMA ME!'
  }
})

export const getters = {
  token (state) {
    return state.auth.token
  },
  client_secret (state) {
    return state.client_secret
  },
  initiativeTypes (state) {
    return state.initiativeTypes
  }
}

export const mutations = {
}

export const actions = {
  async login (context, payload) {
    const loginData = {
      username: payload.form.username,
      password: payload.form.password,
      client_secret: context.getters.client_secret
    }
    // console.log(loginData)
    // const response = await this.$axios.post('auth/token/', loginData)
    await this.$auth.loginWith('local', { data: loginData })
    await this.$axios.setHeader('Authorization', 'Bearer ' + context.getters.token)
    const user = await this.$axios.get('v1/users/me/')
    this.$auth.setUser(user.data)
  },

  async logout () {
    await this.$auth.logout()
  },

  async register (context, payload) {
    const registerData = {
      username: payload.form.username,
      email: payload.form.email,
      password: payload.form.password,
      phone_number: payload.form.phone
    }
    console.log(registerData)
    await this.$axios.post('v1/users/', registerData)
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
    console.log(registerData)
    await this.$axios.post('v1/organizations/', registerData)
  },

  async postComment (context, payload) {
    const newComment = {
      content: payload.content
    }
    await this.$axios.post(`v1/initiatives/${payload.id}/comments/`, newComment)
  },

  async postVote (context, payload) {
    const response = await this.$axios.post(`v1/initiatives/${payload.id}/vote/`)

    if (response.status === 200) {
      return true // voted successfully
    } else if (response.status === 409) {
      return false // already voted
    } else {
      return false // error
    }
  },

  async postCoverImage (context, payload) {
    const formData = new FormData()
    formData.append('image', payload.image)
    const response = await this.$axios.post('v1/images/', formData, {
      headers: {
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
      address: payload.initiativeAddress,
      location: payload.initiativeLocation,
      descriptions: [
        {
          title: 'To je nek title',
          field: 'to_bo_nek_kljuc',
          content: 'to je nek description'
        },
        {
          title: 'To je nek title 2',
          field: 'to_bo_nek_kljuc 2',
          content: 'to je nek description 2'
        }
      ],
      cover_image: payload.initiativeCoverImage,
      uploaded_files: payload.initiativeFiles,
      is_draft: payload.isDraft
    }
    console.log(JSON.stringify(form))
    const response = await this.$axios.post('v1/initiatives/', form)
    const responseData = await response.data

    if (response.status === 201) {
      console.log(responseData)
      return responseData.id
    } else {
      console.log('ni ok', responseData)
      // throw error
    }
  },

  async getInitiatives (context, payload) {
    const params = new URLSearchParams()
    // search
    if (payload.search) {
      params.append('search', payload.search)
    }
    // types
    if (payload.type) {
      params.append('type', payload.type.join(','))
    }
    // areas
    if (payload.area) {
      params.append('area', payload.area.join(','))
    }
    // zones
    if (payload.zone) {
      params.append('area', payload.zone.join(','))
    }
    // statuses
    if (payload.status) {
      params.append('area', payload.status.join(','))
    }
    const response = await this.$axios.get('v1/initiatives/?', { params })
    if (response.status === 200) {
      return { initiatives: response.data }
    } else {
      // console.log('ni ok', responseData)
      // throw error
    }
  },

  async getMyInitiatives (context, payload) {
    const response = await this.$axios.get('v1/initiatives/my')
    if (response.status === 200) {
      return {
        drafts: response.data.drafts,
        published: response.data.published
      }
    } else {
      // console.log('ni ok', responseData)
      // throw error
    }
  },

  async getAreas (context, payload) {
    const response = await this.$axios.get('v1/areas/')
    if (response.status === 200) {
      return await response.data
    } else {
      // console.log('ni ok', responseData)
      // throw error
    }
  },

  async getZones (context, payload) {
    const response = await this.$axios.get('v1/zones/')
    if (response.status === 200) {
      return await response.data
    } else {
      // console.log('ni ok', responseData)
      // throw error
    }
  }
}
