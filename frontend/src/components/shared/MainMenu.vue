<template>
    <div class="flex items-center content-center relative">
    <button
        @click="toggleMenu"
        class="ml-auto mr-auto p-2 btn-icon">
        <icon icon="burger" />
    </button>
    <nav
        class="absolute top-0 left-0 w-0 bg-white z-10 shadow-lg height-nearly-full mb-4 transition-all duration-500"
        :class="{ 'w-64': isOpen, '-ml-20': !isOpen }">
    </nav>
    </div>
</template>
<script>
import Icon from './Icon.vue'
export default {
    name: 'MainMenu',
    components: {
        Icon
    },
    data () {
        return {
            isOpen: false
        }
    },
    methods: {
        toggleMenu () {
            this.isOpen = !this.isOpen
        }
    }
}
</script>
<style scoped>
    .height-nearly-full {
        height: calc(100vh - 150px);
    }
</style>