<template>
  <div class="uk-container">
    <div v-if="loading" class="uk-flex uk-flex-center uk-flex-middle">
      <span uk-spinner="ratio: 5"></span>
    </div>
    <div v-else uk-grid class="uk-child-width-expand@s uk-child-width-1-2@m">
      <div class="uk-position-relative uk-visible-toggle uk-light" tabindex="-1" uk-slideshow>
        <ul class="uk-slideshow-items">
          <li v-for="image in currentItem.images" :key="image.image_url">
            <img :src="image.image_url" :alt="currentItem.name" uk-cover>
          </li>
        </ul>
        <a class="uk-slidenav-large uk-position-center-left uk-position-small" href="#" uk-slidenav-previous uk-slideshow-item="previous"></a>
        <a class="uk-slidenav-large uk-position-center-right uk-position-small" href="#" uk-slidenav-next uk-slideshow-item="next"></a>
      </div>
      <div class="uk-padding">
        <h1 class="uk-heading-medium">{{ currentItem.name }}</h1>
        <p>{{ currentItem.description }}</p>
        <div v-if="currentItem.price.discount > 0">
          <p class="uk-h3"><b><s><em> KES {{ currentItem.price.price }}</em></s> KES {{ currentItem.price.price - currentItem.price.discount }}</b></p>
        </div>
        <div v-else>
          <p class="uk-h3"><b>KES {{ currentItem.price.price }}</b></p>
        </div>
        <div v-if="currentItem.quantity <= 10">
          <p v-if="currentItem.quantity === 0"><em>Out of stock</em></p>
          <p v-else><em>{{ currentItem.quantity }} left in stock</em></p>
        </div>
        <div class="uk-flex uk-flex-center">
          <button class="uk-button tm-button-large uk-button-primary" style="border-radius: 500px" :disabled="currentItem.quantity === 0">Add to cart</button>
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
      quantity: 1
    }
  },
  computed: {
    ...mapGetters('product', {
      currentItem: 'currentItem'
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
    }
  }
}
</script>
