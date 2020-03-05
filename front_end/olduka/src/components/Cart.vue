<template>
  <div>
    <sidenav/>
    <div class="tm-main">
      <div class="uk-container uk-container-small">
        <div v-if="cart.items.length">
          <h3 class="uk-heading-divider">Your Cart</h3>
          <table class="uk-table uk-table-responsive uk-table-justify uk-table-middle uk-table-divider">
            <thead>
              <tr>
                <th></th>
                <th>Item</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Total</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in cart.items" :key="product.item._id">
                <td>
                  <img class="uk-preserve-width" :src="product.item.images[0].image_url" :alt="product.item.name" width="100">
                </td>
                <td>{{product.item.name}}</td>
                <td>KES {{product.item.price.price - product.item.price.discount}}</td>
                <td>
                  <select class="uk-select uk-form-width-small uk-form-blank" @change="updateItemQuantity(product.item, $event)">
                    <option value="product.quantity">{{product.quantity}}</option>
                    <option v-for="i in product.item.quantity" :value="i" :key="i">{{i}}</option>
                  </select>
                </td>
                <td>KES {{(product.item.price.price - product.item.price.discount) * product.quantity}}</td>
                <td><a href="#" uk-icon="trash" @click="removeItem(index)" style="color: #ff0000"></a></td>
              </tr>
              <tr>
                <td style="text-align: right" colspan="6">
                  <h3>Total: KES {{ cartTotal }}</h3>
                </td>
              </tr>
            </tbody>
          </table>
          <p class="uk-text-right" uk-margin>
            <button class="uk-button uk-button-primary uk-button-large uk-border-pill" @click="checkout()">Checkout</button>
          </p>
        </div>
        <div class="uk-text-center" v-else>
          <span uk-icon="icon: cart; ratio: 5"></span>
          <h3 class="uk-margin-medium">Oops! Looks like your cart is empty! Let's shop around and fix that</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters('cart', {
      cart: 'cart',
      cartTotal: 'cartTotal'
    })
  },
  methods: {
    updateItemQuantity (item, e) {
      this.$store.commit('cart/updateCartItemQuantity', { item: item, quantity: e.target.value })
    },
    removeItem (index) {
      this.$store.commit('cart/removeItemFromCart', index)
    },
    checkout () {
      this.$router.push('checkout')
    }
  },
  beforeDestroy () {
    this.$store.dispatch('cart/saveCart')
  }
}
</script>
