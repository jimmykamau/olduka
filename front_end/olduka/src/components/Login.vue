<template>
    <div class="uk-container uk-container-small">
        <div class="uk-heading-divider uk-margin-medium">
            <div class="uk-flex uk-flex-middle uk-margin">
                <div class="uk-flex-1">
                    <h1 class="uk-h1 uk-margin-remove">Log In</h1>
                </div>
                <div class="uk-flex-none uk-text-meta uk-text-nowrap">
                    <span class="uk-visible@s">Don't have an account? </span>
                    <router-link to="/signup">Sign Up</router-link>
                </div>
            </div>
        </div>
        <form class="uk-form-stacked" v-on:submit.prevent>
            <div class="uk-margin">
                <label for="email" class="uk-from-label">Email address</label>
                <input id="email" required class="uk-input" type="email" v-model="credentials.username">
            </div>
            <div class="uk-margin">
                <label for="password" class="uk-form-label">Password</label>
                <input id="password" required class="uk-input" v-model="credentials.password" type="password">
            </div>
            <div uk-grid class="uk-grid-small uk-child-width-expand uk-margin uk-grid">
                <div class="uk-first-column">
                    <input class="uk-checkbox" type="checkbox" id="remember_me" v-model="rememberMe" :value="rememberMe">&nbsp;&nbsp;Remember me
                </div>
                <div>
                    <p class="uk-text-right">
                        <button class="uk-button uk-button-primary uk-button-large uk-border-pill" @click="submit()">Log In</button>
                    </p>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
  data () {
    return {
      credentials: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    submit () {
      this.$store.dispatch('auth/login', this.credentials).then(
        () => {
          const nextURL = this.$route.query.nextURL
          if (nextURL != null) {
            this.$router.push(nextURL)
          } else {
            this.$router.push('/')
          }
          this.$toasted.success(
            'You\'ve successfully logged in'
          )
        }
      ).catch(
        err => {
          this.$toasted.error(
            'There was an error logging you in. Kindly check the credentials you\'ve provided and try again'
          )
          this.error = err
        }
      )
    }
  },
  computed: {
    rememberMe: {
      get () {
        return this.$store.getters['auth/rememberMe']
      },
      set (value) {
        this.$store.commit('auth/remember_me', value)
      }
    }
  },
  mounted () {
    const emailConfirmation = this.$route.query.emailConfirmation
    if (emailConfirmation) {
      this.$toasted.success(
        'Email confirmed successfully. Kindly log in.'
      )
    }
  }
}
</script>
