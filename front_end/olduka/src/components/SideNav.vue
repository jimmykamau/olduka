<template>
  <div class="tm-sidebar-left uk-visible@m">
    <ul v-for="category in productCategories" :key="category._id" class="uk-nav uk-nav-default tm-nav">
      <router-link :to="`/items/${category._id}`" class="uk-nav-header" tag="li"><a><b>{{category.name}}</b></a></router-link>                            
      <router-link v-for="subcategory in category.subcategory" :key="subcategory._id" :to="`/items/${subcategory._id}`" tag="li"><a>{{subcategory.name}}</a></router-link>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters('product', {
      productCategories: 'productCategories'
    })
  },
  created () {
    this.getCategories()
  },
  methods: {
    getCategories () {
      this.$store.dispatch('product/getCategories').then(
        () => {
          this.loading = false
        }
      ).catch(
        err => {
          this.$toasted.error(
            'There was an error fetching categories. Kindly try again later'
          )
          this.$router.go(-1)
        }
      )
    }
  }
}
</script>
