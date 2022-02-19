<template>
    <div class="flex items-center content-center relative" ref="rootEl">
        <button
            @click="toggleMenu"
            class="ml-auto mr-auto p-2 btn-icon">
            <icon icon="burger" />
        </button>
        <nav
            class="absolute top-0 left-0 bg-white z-10 shadow-lg height-nearly-full mb-4 transition-all duration-500 p-4"
            :class="{ 'w-64': isOpen, 'w-0': !isOpen, '-ml-28': !isOpen }">
            <div class="flex flex-col items-start relative">
                <button
                    @click="toggleMenu"
                    class="absolute top-0 right-0 btn-icon">
                    <icon :icon="'close'" :width="16" :height="16"/>
                </button>
                <span class="flex mb-2 w-full border-grey-300 border-b pb-2"><icon class="text-teal-500 mr-2" :icon="'sun'" />Hi {{ user.username }}!</span>
                <router-link :to="{ name: 'logout' }" class="text-blue-500 hover:text-blue-700 mb-8">
                    Log out <icon :icon="'logout'" class="inline ml-2" />
                </router-link>
                <router-link
                    class="link mb-8"
                    :to="{ name: 'dashboard' }">
                Dashboard
            </router-link>
            </div>
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