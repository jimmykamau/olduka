<template>
  <div class="uk-grid-match uk-grid-collapse" uk-grid>
    <div class="uk-container uk-width-3-4@m">
      <CheckoutInformation />
    </div>
    <div class="uk-container uk-width-1-4@m">
      <OrderSummary />
    </div>
  </div>
</template>

<script>
import OrderSummary from '@/components/OrderSummary.vue'
import CheckoutInformation from '@/components/CheckoutInformation.vue'

export default {
  components: {
    OrderSummary,
    CheckoutInformation
  }
}
</script>
