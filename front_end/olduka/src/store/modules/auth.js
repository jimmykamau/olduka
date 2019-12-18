import axios from 'axios'
import VueCookies from 'vue-cookies'

const state = {
  rememberMe: VueCookies.get('rememberMe') || false,
  token: VueCookies.get('authToken') || '',
  user: VueCookies.get('userDetails') || {}
}

const mutations = {
  remember_me (state, remember) {
    state.rememberMe = remember
    if (remember) {
      VueCookies.set('rememberMe', remember, '1d')
    } else {
      VueCookies.remove('rememberMe')
    }
  },
  auth_success (state, { token, user }) {
    state.token = token
    state.user = user
    axios.defaults.headers.common['Authorization'] = 'JWT ' + token
    if (state.rememberMe) {
      VueCookies.set('authToken', token, '1d')
      VueCookies.set('userDetails', user, '1d')
    } else {
      VueCookies.remove('authToken')
      VueCookies.remove('userDetails')
    }
  },
  update_success (state, user) {
    state.user = user
    if (state.rememberMe) {
      VueCookies.set('userDetails', user, '1d')
    }
  },
  logout (state) {
    state.token = ''
    state.user = {}
    VueCookies.keys().forEach(
      cookie => VueCookies.remove(cookie)
    )
    delete axios.defaults.headers.common['Authorization']
  }
}

const actions = {
  login ({ commit, dispatch }, user) {
    return new Promise((resolve, reject) => {
      axios({
        url: 'auth/login/',
        data: user,
        method: 'POST'
      }).then(resp => {
        const token = resp.data.token
        const user = resp.data.user
        commit('auth_success', { token, user })
        dispatch('cart/getCart', null, { root: true })
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  },
  logout ({ commit }) {
    return new Promise((resolve, reject) => {
      axios({
        url: 'auth/logout/',
        method: 'GET'
      }).then(resp => {
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
      commit('logout')
    })
  },
  signup ({ commit }, user) {
    return new Promise((resolve, reject) => {
      axios({
        url: 'auth/user/create/',
        data: user,
        method: 'POST'
      }).then(resp => {
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  },
  resendEmailConfirmation ({ commit }, email) {
    return new Promise((resolve, reject) => {
      axios({
        url: 'auth/verify-email/',
        data: email,
        method: 'POST'
      }).then(resp => {
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  },
  getUserInfo ({ commit }) {
    return new Promise((resolve, reject) => {
      axios({
        url: `auth/user/${encodeURIComponent(state.user.id)}/`,
        method: 'GET'
      }).then(resp => {
        const user = resp.data
        commit('update_success', user)
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  },
  updateUserInfo ({ commit }, user) {
    return new Promise((resolve, reject) => {
      axios({
        url: `auth/user/${state.user.id}/`,
        data: user,
        method: 'PATCH'
      }).then(resp => {
        const user = resp.data
        commit('update_success', user)
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  },
  refreshToken ({ commit }) {
    return new Promise((resolve, reject) => {
      axios({
        url: 'auth/token/refresh/',
        data: { 'token': state.token },
        method: 'POST'
      }).then(resp => {
        const token = resp.data.token
        const user = resp.data.user
        commit('auth_success', { token, user })
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  }
}

const getters = {
  isLoggedIn: state => !!state.token,
  rememberMe: state => state.rememberMe
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
