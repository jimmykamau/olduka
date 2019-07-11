<template>
    <div>
        <div class="uk-navbar-container tm-navbar-container" uk-sticky="media: 960">
            <div class="uk-container uk-container-expand">
                <nav class="uk-navbar" uk-navbar>

                    <div class="uk-navbar-left">

                        <router-link class="uk-navbar-item uk-logo" to="/">
                            <canvas class="uk-margin-small-right" width="28" height="34" uk-svg src="../assets/section-background.svg"></canvas> Olduka
                        </router-link>

                    </div>

                    <div class="uk-navbar-center">

                        <ul class="uk-navbar-nav uk-visible@m">
                            <li>
                                <a href="#">Parent</a>
                                <div class="uk-navbar-dropdown">
                                    <ul class="uk-nav uk-navbar-dropdown-nav">
                                        <li class="uk-active"><a href="#">Active</a></li>
                                        <li><a href="#">Item</a></li>
                                        <li class="uk-nav-header">Header</li>
                                        <li><a href="#">Item</a></li>
                                        <li><a href="#">Item</a></li>
                                        <li class="uk-nav-divider"></li>
                                        <li><a href="#">Item</a></li>
                                    </ul>
                                </div>
                            </li>
                            <li><a href="/">Documentation</a></li>
                            <router-link to="/" tag="li"><a>Changelog</a></router-link>
                        </ul>

                    </div>

                    <div class="uk-navbar-right">
                        <a class="uk-navbar-toggle" href="#modal-full" uk-search-icon uk-toggle></a>
                        <ul class="uk-navbar-nav">
                            <li>
                                <a href="#" class="tm-button-default uk-icon"><canvas uk-icon="icon: cart" width="20" height="20"></canvas></a>
                                <div class="uk-navbar-dropdown">
                                    <p>Your cart is empty</p>
                                </div>
                            </li>
                        </ul>
                        <div v-if="!isLoggedIn" class="uk-navbar-item uk-visible@m">
                            <router-link class="uk-button tm-button-default" to="/login">Log In</router-link>
                            <router-link class="uk-button uk-button-default tm-button-default" to="/signup" active-class="page-active">Sign Up</router-link>
                        </div>
                        <ul v-else class="uk-navbar-nav uk-visible@m">
                            <li>
                                <a href="#" class="tm-button-default uk-icon"><canvas uk-icon="icon: user" width="20" height="20"></canvas></a>
                                <div class="uk-navbar-dropdown">
                                    <ul class="uk-nav uk-navbar-dropdown-nav">
                                        <li class="uk-nav-header">Hello, {{ user.first_name }}</li>
                                        <li class="uk-nav-divider"></li>
                                        <router-link to="/account" tag="li"><a>My account</a></router-link>
                                        <li><a @click="logout">Log Out</a></li>
                                    </ul>
                                </div>
                            </li>
                        </ul>

                        <a class="uk-navbar-toggle uk-hidden@m" uk-navbar-toggle-icon href="#offcanvas" uk-toggle></a>

                    </div>

                </nav>
            </div>
        </div>

        <div id="modal-full" class="uk-modal-full uk-modal" uk-modal>
            <div class="uk-modal-dialog uk-flex uk-flex-center uk-flex-middle" uk-height-viewport>
                <button class="uk-modal-close-full" type="button" uk-close></button>
                <form class="uk-search uk-search-large">
                    <input class="uk-search-input uk-text-center" type="search" placeholder="Search..." autofocus>
                </form>
            </div>
        </div>

        <div id="offcanvas" uk-offcanvas="mode: push; overlay: true">
            <div class="uk-offcanvas-bar">
                <div class="uk-panel">

                    <ul class="uk-nav uk-nav-default tm-nav" v-if="isLoggedIn">
                        <li class="uk-nav-header">Hello {{ user.first_name }}</li>
                        <router-link to="/account" tag="li"><a>My account</a></router-link>
                        <li><a @click="logout">Log Out</a></li>
                    </ul>
                    <ul class="uk-nav uk-nav-default tm-nav" v-else>
                        <router-link class="uk-button tm-button-default" to="/login">Log In</router-link>
                        <router-link class="uk-button uk-button-default tm-button-default" to="/signup" active-class="page-active">Sign Up</router-link>
                    </ul>

                    <!-- <ul class="uk-nav uk-nav-default tm-nav uk-margin-top" v-for="(pages, category, index) in navigation">
                        <li class="uk-nav-header">{{category}}</li>
                        <li v-for="(p, label) in pages" exact><a :href="'./'+p">{{label}}</a></li>
                    </ul> -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'

export default {
  computed: {
    ...mapState('auth', {
      user: state => state.user
    }),
    ...mapGetters('auth', {
      isLoggedIn: 'isLoggedIn'
    })
  },
  methods: {
    logout: function () {
      this.$store.dispatch('auth/logout').then(
        () => {
          this.$toasted.success(
            'You\'ve successfully logged out'
          )
          this.$router.push({ name: 'home' })
        }
      )
    }
  }
}
</script>
