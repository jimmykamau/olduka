<template>
  <div>
    <div v-if="loading" class="uk-flex uk-flex-center uk-flex-middle">
      <span uk-spinner="ratio: 5"></span>
    </div>
    <div uk-grid>
      <div class="uk-width-1-4@m">
        <sidenav/>
      </div>
      <div v-if="!loading" class="uk-width-3-4@m uk-width-expand@s">
        <div class="uk-container">
          <div uk-grid>
            <div class="uk-width-1-1 uk-child-width-expand@s" uk-grid>
              <div>
                <div class="uk-position-relative uk-visible-toggle uk-light" tabindex="-1" uk-slideshow="ratio: 300:300">
                  <ul class="uk-slideshow-items">
                    <li v-for="image in currentItem.images" :key="image.image_url">
                      <img :src="image.image_url" :alt="currentItem.name" uk-cover>
                    </li>
                  </ul>
                  <a class="uk-slidenav-large uk-position-center-left uk-position-small" href="#" uk-slidenav-previous uk-slideshow-item="previous"></a>
                  <a class="uk-slidenav-large uk-position-center-right uk-position-small" href="#" uk-slidenav-next uk-slideshow-item="next"></a>
                </div>
              </div>
              <div class="uk-flex uk-flex-column uk-flex-middle uk-flex-center">
                <div>
                  <h1 class="uk-heading-small">{{ currentItem.name }}</h1>
                </div>
                <div>
                  <p class="uk-h3">
                    <b v-if="currentItem.price.discount > 0">
                      <s><em> KES {{ currentItem.price.price }}</em></s> KES {{ currentItem.price.price - currentItem.price.discount }}
                    </b>
                    <b v-else>KES {{ currentItem.price.price }}</b>
                  </p>
                </div>
                <div v-if="currentItem.quantity <= 10">
                  <p>
                    <em v-if="currentItem.quantity === 0">Out of stock</em>
                    <em v-else>{{ currentItem.quantity }} left in stock</em>
                  </p>
                </div>
                <div class="uk-flex@m uk-flex-middle@m">
                  <div v-if="isLoggedIn" uk-grid>
                    <div v-if="currentItem.quantity > 0">
                      <select class="uk-select uk-form-width-small" v-model="quantity">
                        <option value="1" disabled>Quantity: 1</option>
                        <option v-for="i in currentItem.quantity" :value="i" :key="i">{{ i }}</option>
                      </select>
                    </div>
                    <div>
                      <button v-if="isLoggedIn" class="uk-button tm-button-large uk-button-primary" style="border-radius: 500px" :disabled="currentItem.quantity === 0" @click="addToCart()">Add to cart</button>
                    </div>
                  </div>
                  <div v-else>
                    <p>Kindly <router-link to="/signup">sign up</router-link>/<router-link :to="{ name: 'login', query: { nextURL: currentRoute } }">log in</router-link> to purchase</p>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <p>{{ currentItem.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      loading: false,
      quantity: 1,
      currentRoute: this.$route.currentRoute
    }
  },
  computed: {
    ...mapGetters('product', {
      currentItem: 'currentItem'
    }),
    ...mapGetters('auth', {
      isLoggedIn: 'isLoggedIn'
    })
  },
  created () {
    this.getItemDetails()
  },
  watch: {
    '$route': 'getItemDetails'
  },
  methods: {
    getItemDetails () {
      this.loading = true
      this.$store.dispatch('product/getItemDetails', this.$route.params.item_id).then(
        () => {
          this.loading = false
        }
      ).catch(
        err => {
          this.$toasted.error(
            'There was an error fetching details for the item. Kindly try again later'
          )
          this.$router.go(-1)
        }
      )
    },
    addToCart () {
      let currentItem = this.currentItem
      let quantity = this.quantity
      this.$store.commit('cart/addItemToCart', { item: currentItem, quantity: quantity })
      this.$toasted.success(
        quantity + ' ' + currentItem.name + ' added to cart'
      )
    }
  }
}
</script>
