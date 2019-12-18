import axios from 'axios'
import VueCookies from 'vue-cookies'

const state = {
  cart: VueCookies.get('cart') || { items: [] }
}

const mutations = {
  addItemToCart (state, { item, quantity }) {
    var itemInCart = state.cart.items.find(
      product => product.item._id === item._id
    )
    if (itemInCart) {
      let maxQuantity = item.quantity
      let newQuantity = itemInCart.quantity + quantity
      if (newQuantity <= maxQuantity) {
        itemInCart.quantity = newQuantity
      }
    } else {
      state.cart.items.push(
        { item: item, quantity: quantity }
      )
    }
    VueCookies.set('cart', state.cart, '0')
  },
  updateCartItemQuantity (state, { item, quantity }) {
    let itemInCart = state.cart.items.find(
      product => product.item._id === item._id
    )
    if (itemInCart && quantity <= item.quantity) {
      itemInCart.quantity = quantity
    }
    VueCookies.set('cart', state.cart, '0')
  },
  removeItemFromCart (state, index) {
    state.cart.items.splice(index, 1)
    VueCookies.set('cart', state.cart, '0')
  },
  setCart (state, cart) {
    state.cart = cart
    VueCookies.set('cart', cart, '0')
  }
}

const actions = {
  getCart ({ commit }) {
    return new Promise((resolve, reject) => {
      axios({
        url: 'cart/create/',
        method: 'POST'
      }).then(resp => {
        const cart = resp.data
        commit('setCart', cart)
        resolve(resp)
      }).catch(err => {
        reject(err)
      })
    })
  },
  saveCart ({ commit }) {
    console.log('Saving cart')
    return new Promise((resolve, reject) => {
      axios({
        url: `cart/${state.cart._id}/`,
        data: { 'items': state.cart.items },
        method: 'PUT'
      }).then(resp => {
        const cart = resp.data
        commit('setCart', cart)
        resolve(resp)
      }).catch(err => reject(err))
    })
  }
}

const getters = {
  cart: state => state.cart
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
