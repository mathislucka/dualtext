<template>
    <div class="flex items-center content-center relative" ref="rootEl">
        <button
            @click="toggleMenu"
            class="ml-auto mr-auto p-2 btn-icon">
            <icon icon="burger" />
        </button>
        <nav
            class="absolute top-0 left-0 w-0 bg-white z-10 shadow-lg height-nearly-full mb-4 transition-all duration-500 flex flex-col p-4 items-start"
            :class="{ 'w-64': isOpen, '-ml-20': !isOpen }">
            <span class="flex mb-2 w-full border-grey-300 border-b pb-2"><icon class="text-teal-500 mr-2" :icon="'sun'" />Hi {{ user.username }}!</span>
            <button class="text-blue-500 hover:text-blue-700 mb-8">Log out <icon :icon="'logout'" class="inline ml-2" /></button>
            <div class="flex flex-col items-start" id="menu-content" />
        </nav>
    </div>
</template>
<script>
import Icon from './Icon.vue'
import { useUser } from './../../composables/useUser.js'
import { useClickOutside } from './../../composables/useClickOutside.js'
import { ref } from 'vue'

export default {
    name: 'MainMenu',
    components: {
        Icon
    },
    methods: {
        toggleMenu () {
            if (!this.isOpen) {
                this.isOpen = true
                this.registerClickEvent()
            } else if (this.isOpen) {
                this.isOpen = false
                this.unregisterClickEvent()
            }
        }
    },
    setup () {
        const { user } = useUser()
        const isOpen = ref(false)
        const rootEl = ref(null)
        const { registerClickEvent, unregisterClickEvent } = useClickOutside(rootEl, isOpen)
        return {
            isOpen,
            user,
            rootEl,
            registerClickEvent,
            unregisterClickEvent
        }
    }
}
</script>
<style scoped>
    .height-nearly-full {
        height: calc(100vh - 150px);
    }
</style>