<template>
    <div class="uk-width-1-1 uk-margin-remove" uk-height-viewport>
        <div class="uk-container">
            <ul uk-tab>
                <li><a href="#">Profile</a></li>
            </ul>

            <ul class="uk-switcher uk-margin">
                <li><Profile /></li>
            </ul>
        </div>
    </div>
</template>

<script>
import Profile from '@/components/Profile.vue'
export default {
  components: {
    Profile
  }
}
</script>
