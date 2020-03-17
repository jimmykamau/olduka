<template>
  <div class="uk-grid-match" uk-grid>
    <div class="uk-container uk-width-3-4@m">
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
          <div class="uk-margin" v-show="shippingAddress['locality']">
              <label for="delivery_option" class="uk-form-label">Delivery option *</label>
              <select class="uk-select" id="delivery_option" v-model="selectedShippingOption">
                <option v-for="option in shippingOptions" :value="option" :key="option['name']">{{ option['name'] }} (KES {{ option['cost'] }})</option>
              </select>
          </div>
          <div class="uk-margin" id="apartment_details" v-show="selectedShippingOption && selectedShippingOption['name'] === 'Expedited'">
              <label for="apartment" class="uk-form-label">Apartment, suite, etc.</label>
              <input id="apartment" class="uk-input">
          </div>
        </form>
      </div>
    </div>
    <div class="uk-container uk-container-small uk-width-1-4@m">
      <div class="uk-card uk-card-default">
        <div class="uk-card-header">
          <h3 class="uk-card-title">Order summary</h3>
        </div>
        <div class="uk-card-body">
          <table class="uk-table">
            <tbody>
              <tr>
                <td><b>Subtotal</b></td>
                <td>KES {{ cartTotal }}</td>
              </tr>
              <tr>
                <td><b>Shipping</b></td>
                <td>KES {{ selectedShippingOption != null ? selectedShippingOption['cost'] : 0 }}</td>
              </tr>
              <tr class="uk-h4">
                <td>Order total</td>
                <td>KES {{ cartTotal }}</td>
              </tr>
            </tbody>
          </table>
          <button class="uk-button uk-button-primary uk-button-large uk-border-pill" :disabled="selectedShippingOption === null">Place order</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

export default {
  data () {
    return {
      placeDetails: null,
      shippingAddress: {
        locality: null
      },
      selectedShippingOption: null,
      shippingOptions: [
        {
          name: 'Expedited',
          cost: '300'
        }
      ]
    }
  },
  computed: {
    ...mapState('auth', {
      user: state => state.user
    }),
    ...mapGetters('cart', {
      cart: 'cart',
      cartTotal: 'cartTotal'
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
        ['address_components', 'formatted_address', 'geometry', 'name']
      )
      this.autocomplete.addListener('place_changed', this.onPlaceChanged)
    }
  },
  methods: {
    onPlaceChanged () {
      this.selectedShippingOption = null
      let expedited = {
        name: 'Expedited',
        cost: '300'
      }
      let pickup = {
        name: 'Pickup in CBD',
        cost: '0'
      }
      this.shippingOptions = [expedited]
      let place = this.autocomplete.getPlace()
      this.placeDetails = place
      for (const component in place.address_components) {
        if (place.address_components[component].types[0] === 'locality') {
          this.shippingAddress['locality'] = place.address_components[component].long_name
          if (this.shippingAddress['locality'] === 'Nairobi') {
            this.shippingOptions.push(pickup)
          } else {
            this.shippingOptions = [expedited]
          }
        }
      }
    }
  }
}
</script>
