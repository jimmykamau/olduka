<template>
  <div class="uk-container">
    <div class="uk-flex uk-flex-center">
      <form class="uk-form-stacked" v-on:submit.prevent>
        <legend class="uk-legend">Contact Information</legend>
        <div uk-grid class="uk-grid-small uk-child-width-expand uk-margin uk-grid">
            <div class="uk-first-column">
                <label for="contact_firstname" class="uk-form-label">First name *</label>
                <input id="contact_firstname" required class="uk-input" :value="user.first_name">
            </div>
            <div>
                <label for="contact_lastname" class="uk-form-label">Last name *</label>
                <input id="contact_lastname" required class="uk-input" :value="user.last_name">
            </div>
        </div>
        <div class="uk-margin">
            <label for="contact_email" class="uk-form-label">Email address *</label>
            <input id="contact_email" required class="uk-input" type="email" :value="user.email">
        </div>
        <div class="uk-margin">
            <label for="contact_mobile" class="uk-form-label">Mobile number</label>
            <input id="contact_mobile" class="uk-input" type="tel" :value="user.user_profile.mobile">
        </div>
        <hr class="uk-hr" />
        <legend class="uk-legend">Shipping Information</legend>
        <div class="uk-margin">
            <label for="shipping_address_search" class="uk-form-label">Shipping address *</label>
            <input id="shipping_address_search" required class="uk-input">
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data () {
    return {
      shippingAddress: null
    }
  },
  computed: {
    ...mapState('auth', {
      user: state => state.user
    })
  },
  mounted () {
    let mapsAPIURL = 'https://maps.googleapis.com/maps/api/js?libraries=places&callback=onAPIsLoaded&key=' + process.env.VUE_APP_PLACES_API_KEY
    let mapsAPIScript = document.createElement('script')
    mapsAPIScript.setAttribute('src', mapsAPIURL)
    document.head.appendChild(mapsAPIScript)
    window['onAPIsLoaded'] = () => {
      this.autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('shipping_address_search'),
        {
          componentRestrictions: {
            country: 'ke'
          }
        }
      )
      this.autocomplete.setFields(
        ['formatted_address', 'geometry', 'name']
      )
      this.autocomplete.addListener('place_changed', this.onPlaceChanged)
    }
  },
  methods: {
    onPlaceChanged () {
      let place = this.autocomplete.getPlace()
      this.shippingAddress = place
    }
  }
}
</script>
