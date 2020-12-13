<template>
        <toast-bar />
        <router-view />
</template>

<script>
import ToastBar from './components/shared/ToastBar.vue'
import { UserStore } from './store/User.js'

export default {
  name: 'App',
  components: {
    ToastBar,
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
