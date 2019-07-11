<template>
    <div class="uk-card uk-card-body">
        <form class="uk-form-horizontal" v-on:submit.prevent>
            <div class="uk-margin">
                <label for="firstname" class="uk-form-label">First Name</label>
                <div class="uk-form-controls">
                    <input id="firstname" required class="uk-input uk-form-blank" v-model="credentials.first_name">
                </div>
            </div>
            <div class="uk-margin">
                <label for="lastname" class="uk-form-label">Last Name</label>
                <div class="uk-form-controls">
                    <input id="lastname" required class="uk-input uk-form-blank" v-model="credentials.last_name">
                </div>
            </div>
            <div class="uk-margin">
                <label class="uk-form-label" for="form-horizontal-text">Mobile number</label>
                <div class="uk-form-controls">
                    <input class="uk-input uk-form-blank" id="mobile" type="tel" v-model="credentials.user_profile.mobile" placeholder="You do not have a phone number associated with your account">
                </div>
            </div>
            <p class="uk-text-right">
                <button class="uk-button uk-button-primary uk-button-large uk-border-pill" @click="submit()">Update</button>
            </p>
        </form>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data () {
    return {
      credentials: {
        first_name: '',
        last_name: '',
        user_profile: {
          mobile: null
        }
      }
    }
  },
  methods: {
    submit () {
      var user = this.credentials
      this.$store.dispatch('auth/updateUserInfo', user).then(
        () => this.$toasted.success('Your details have been updated successfully!')
      ).catch(
        err => {
          this.$toasted.error('Oops! Something went wrong while updating your details. Please try again')
          this.error = err
        }
      )
    }
  },
  computed: {
    ...mapState('auth', {
      user: state => state.user
    })
  },
  mounted () {
    this.credentials.first_name = this.user.first_name
    this.credentials.last_name = this.user.last_name
    this.credentials.user_profile.mobile = this.user.user_profile.mobile
  }
}
</script>
