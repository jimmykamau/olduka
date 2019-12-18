<template>
  <div>
    <sidenav/>
    <div class="tm-main">
      <div class="uk-container uk-container-small">
        <div v-if="loading" class="uk-flex uk-flex-center uk-flex-middle">
          <span uk-spinner="ratio: 5"></span>
        </div>
        <div v-else>
          <div uk-grid="masonry: true" class="uk-flex-center">
            <div class="uk-flex uk-flex-center" v-for="item in categoryItems.category_item" :key="item._id">
              <router-link :to="`/item/${item._id}`" class="uk-card uk-card-hover uk-link-toggle">
                <div class="uk-card-media-top">
                  <img :src="item.images[0].image_url">
                </div>
                <div class="uk-card-body">
                  <h3 class="uk-card-title"><span class="uk-link-heading">{{ item.name }}</span></h3>
                  <div v-if="item.price.discount > 0">
                    <p><s><em><b> KES {{ item.price.price }}</b></em></s><b> KES {{ item.price.price - item.price.discount }}</b></p>
                  </div>
                  <div v-else>
                    <p><b>KES {{ item.price.price }}</b></p>
                  </div>
                </div>
              </router-link>
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
      loading: false
    }
  },
  computed: {
    ...mapGetters('product', {
      categoryItems: 'categoryItems'
    })
  },
  created () {
    this.getItems()
  },
  watch: {
    '$route': 'getItems'
  },
  methods: {
    getItems () {
      this.loading = true
      this.$store.dispatch('product/getCategoryItems', this.$route.params.category_id).then(
        () => {
          this.loading = false
        }
      ).catch(
        err => {
          this.$toasted.error(
            'There was an error fetching items in the category. Kindly try again later'
          )
          this.$router.go(-1)
        }
      )
    }
  }
}
</script>
