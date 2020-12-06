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

export default {
  name: 'App',
  components: {
    ToastBar,
    PageHeader,
  }
}
</script>

<style>
@import "assets/css/main.css";
</style>
