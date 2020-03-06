<template>
  <div class="uk-container uk-container-small">
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
              <td>Calculated at next step</td>
            </tr>
            <tr class="uk-h4">
              <td>Order total</td>
              <td>KES {{ cartTotal }}</td>
            </tr>
          </tbody>
        </table>
        <button class="uk-button uk-button-primary uk-button-large uk-border-pill">Place order</button>
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
  }
}
</script>
