import Vue from 'vue'
import Router from 'vue-router'
import store from './store'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./views/Home.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('./views/About.vue')
    },
    {
      path: '/account',
      name: 'account',
      component: () => import('./views/Account.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./components/Login.vue'),
      meta: {
        onlyWhenLoggedOut: true
      }
    },
    {
      path: '/signup',
      name: 'sign-up',
      component: () => import('./components/Signup.vue'),
      meta: {
        onlyWhenLoggedOut: true
      }
    },
    {
      path: '/successful-signup',
      name: 'successful-signup',
      component: () => import('./components/SuccessfulSignup.vue')
    },
    {
      path: '/resend-email-confirmation',
      name: 'resend-email-confirmation',
      component: () => import('./components/ResendEmailConfirmation.vue')
    },
    {
      path: '/category/:category_id/items',
      name: 'list-category-items',
      component: () => import('./components/ListCategoryItems.vue')
    },
    {
      path: '/items',
      name: 'items',
      component: () => import('./components/ListItems.vue')
    },
    {
      path: '/item/:item_id',
      name: 'item-details',
      component: () => import('./components/SingleItem.vue')
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('./components/Cart.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '*',
      name: 'not-found',
      component: () => import('./views/404.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const onlyWhenLoggedOut = to.matched.some(record => record.meta.onlyWhenLoggedOut)
  const isLoggedIn = store.getters['auth/isLoggedIn']

  if (requiresAuth && !isLoggedIn) {
    return next({
      path: '/login',
      query: { nextURL: to.fullPath }
    })
  }

  if (isLoggedIn && onlyWhenLoggedOut) {
    return next('/')
  }

  next()
})

export default router
