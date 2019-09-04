import axios from 'axios'
import VueCookies from 'vue-cookies'

const state = {
  productCategories: VueCookies.get('productCategories') || [],
  categoryItems: {},
  currentItem: {}
}

const mutations = {
  updateCategories (state, categories) {
    state.productCategories = categories
    VueCookies.set('productCategories', categories, '0')
  },
  updateCategoryItems (state, items) {
    state.categoryItems = items
  },
  updateCurrentItemDetails (state, item) {
    state.currentItem = item
  }
}

const actions = {
  getCategories ({ commit }) {
    return new Promise((resolve, reject) => {
      axios({
        url: 'product/category/',
        method: 'GET'
      }).then(resp => {
        const categories = resp.data
        commit('updateCategories', categories)
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  },
  getCategoryItems ({ commit }, categoryID) {
    return new Promise((resolve, reject) => {
      axios({
        url: `product/category/${categoryID}/item/`,
        method: 'GET'
      }).then(resp => {
        const categoryDetails = resp.data
        commit('updateCategoryItems', categoryDetails)
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  },
  getItemDetails ({ commit }, itemID) {
    return new Promise((resolve, reject) => {
      axios({
        url: `product/item/${itemID}/`,
        method: 'GET'
      }).then(resp => {
        const itemDetails = resp.data
        commit('updateCurrentItemDetails', itemDetails)
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  }
}

const getters = {
  productCategories: state => state.productCategories,
  categoryItems: state => state.categoryItems,
  currentItem: state => state.currentItem
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
