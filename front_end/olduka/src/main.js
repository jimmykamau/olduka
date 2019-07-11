import Vue from 'vue'
import Axios from 'axios'
import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons.min.js'
import Toasted from 'vue-toasted'
import VueCookies from 'vue-cookies'
import App from './App.vue'
import router from './router'
import store from './store'

import Navbar from './components/Navbar.vue'

Vue.config.productionTip = false
Vue.use(Toasted, { duration: 5000, keepOnHover: true })
Vue.use(VueCookies)
UIkit.use(Icons)

Vue.prototype.$http = Axios
Vue.prototype.$http.defaults.baseURL = process.env.VUE_APP_BACKEND_URL
Vue.prototype.$http.defaults.xsrfCookieName = 'csrftoken'
Vue.prototype.$http.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

const userToken = VueCookies.get('authToken')
if (userToken) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = 'JWT ' + userToken
  store.dispatch('auth/getUserInfo').catch(
    err => {
      store.dispatch('auth/refreshToken').catch(
        err => {
          store.dispatch('auth/logout')
      })
    }
  )
}

Vue.component('navbar', Navbar)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
