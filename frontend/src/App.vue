<template>
    <div class="h-screen w-full">
        <toast-bar />
        <page-header v-if="false" />
        <router-view />
    </div>
</template>

<script>
import PageHeader from './components/shared/PageHeader.vue'
import ToastBar from './components/shared/ToastBar.vue'
import { UserStore } from './store/User.js'

export default {
  name: 'App',
  components: {
    ToastBar,
    PageHeader,
  },
  mounted () {
      if (sessionStorage.getItem('auth_token')) {
          UserStore.actions.fetchCurrentUser()
      }
  }
}
</script>

<style>
@import "assets/css/main.css";
</style>
