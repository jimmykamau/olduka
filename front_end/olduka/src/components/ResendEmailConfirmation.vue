<template>
    <div class="uk-container uk-container-small">
        <div class="uk-heading-divider uk-margin-medium">
            <div class="uk-flex uk-flex-middle uk-margin">
                <div class="uk-flex-1">
                    <h1 class="uk-h1 uk-margin-remove">Resend Activation Link</h1>
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
                <input id="email" required class="uk-input" type="email" v-model="email">
            </div>
            <p class="uk-text-right">
                <button class="uk-button uk-button-primary uk-button-large uk-border-pill" @click="submit()">Send</button>
            </p>
        </form>
        <p class="uk-text-medium uk-text-muted">Already confirmed your address? <router-link to="/login">Log In</router-link></p>
    </div>
</template>

<script>
export default {
  data () {
    return {
      email: ''
    }
  },
  methods: {
    submit () {
      var data = { email: this.email }
      this.$store.dispatch('auth/resendEmailConfirmation', data).then(
        () => {
          this.$router.push('/successful-signup')
        }
      ).catch(
        err => {
          var errorMessage = 'Oops! Something went wrong. Please try again after a minute.'
          if (err.response.data.detail.email) {
            errorMessage = err.response.data.detail.email
          }
          this.$toasted.error(
            errorMessage
          )
        }
      )
    }
  }
}
</script>
