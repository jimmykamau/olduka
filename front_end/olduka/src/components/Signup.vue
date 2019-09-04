<template>
    <div class="uk-container uk-container-small">
        <div class="uk-heading-divider uk-margin-medium">
            <div class="uk-flex uk-flex-middle uk-margin">
                <div class="uk-flex-1">
                    <h1 class="uk-h1 uk-margin-remove">Sign Up</h1>
                </div>
                <div class="uk-flex-none uk-text-meta uk-text-nowrap">
                    <span class="uk-visible@s">Already have an account? </span>
                    <router-link to="/login">Log In</router-link>
                </div>
            </div>
        </div>
        <form class="uk-form-stacked" v-on:submit.prevent>
            <div uk-grid class="uk-grid-small uk-child-width-expand uk-margin uk-grid">
                <div class="uk-first-column">
                    <label for="firstname" class="uk-form-label">First name *</label>
                    <input id="firstname" required class="uk-input" v-model="credentials.first_name">
                </div>
                <div>
                    <label for="lastname" class="uk-form-label">Last name *</label>
                    <input id="lastname" required class="uk-input" v-model="credentials.last_name">
                </div>
            </div>
            <div class="uk-margin">
                <label for="email" class="uk-form-label">Email address *</label>
                <input id="email" required class="uk-input" type="email" v-model="credentials.email">
            </div>
            <div class="uk-margin">
                <label for="password" class="uk-form-label">Password *</label>
                <input id="password" required class="uk-input" v-model="credentials.password" type="password">
            </div>
            <div class="uk-margin">
                <label for="mobile" class="uk-form-label">Mobile number</label>
                <input id="mobile" class="uk-input" type="tel" v-model="credentials.user_profile.mobile">
            </div>
            <p class="uk-text-right">
                <button class="uk-button uk-button-primary uk-button-large uk-border-pill" @click="submit()">Sign Up</button>
            </p>
        </form>
    </div>
</template>

<script>
export default {
  data () {
    return {
      credentials: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        user_profile: {
          mobile: null
        }
      }
    }
  },
  methods: {
    submit () {
      var credentials = {
        first_name: this.credentials.first_name,
        last_name: this.credentials.last_name,
        email: this.credentials.email,
        password: this.credentials.password,
        user_profile: this.credentials.user_profile
      }
      this.$store.dispatch('auth/signup', credentials).then(
        () => this.$router.push('/successful-signup')
      ).catch(
        err => {
          var errorMessage = 'Oops! Something went wrong. Please try again after a minute.'
          if (err.response.data.email) {
            errorMessage = err.response.data.email
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
