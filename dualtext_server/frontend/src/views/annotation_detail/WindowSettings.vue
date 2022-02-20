<template>
    <div class="text-right">
        <button
            @click="setOrientation('horizontal')"
            class="ml-auto mr-2 p-1 btn-icon"
            :class="{'btn-active': currentOrientation === 'horizontal' }">
            <icon icon="columns" :height="16" :width="16" class="rotate-90" />
        </button>
        <button
            @click="setOrientation('vertical')"
            class="ml-auto mr-2 p-1 btn-icon"
            :class="{'btn-active': currentOrientation === 'vertical' }">
            <icon icon="columns" :height="16" :width="16" />
        </button>
        <button
            @click="toggleScreenSize"
            class="ml-auto mr-1 p-1 btn-icon">
            <icon :icon="iconType" :width="16" :height="16" />
        </button>
    </div>
</template>

<script>
import {computed, ref} from 'vue'
import Icon from '../../components/shared/Icon.vue'

export default {
    name: 'WindowSettings',
    emits: [ 'change-orientation', 'change-screen-size' ],
    components: {
        Icon
    },
    setup (_, { emit }) {
        const defaultOrientation = 'horizontal'
        const defaultScreenSize = 'normal'
        const getOrientation = () => {
            const orientation = window.localStorage.getItem('orientation')
            emit('change-orientation', orientation || defaultOrientation)
            return orientation || defaultOrientation
        }

        const getScreenSize = () => {
            const size = window.localStorage.getItem('screenSize')
            emit('change-screen-size', size || defaultScreenSize)
            return size || defaultScreenSize
        }

        const currentOrientation = ref(getOrientation())
        const currentScreenSize = ref(getScreenSize())

        const setOrientation = (orientation) => {
            currentOrientation.value = orientation
            emit('change-orientation', currentOrientation.value)
            window.localStorage.setItem('orientation', currentOrientation.value)
        }

        const toggleScreenSize = () => {
            currentScreenSize.value = currentScreenSize.value === 'normal' ? 'full' : 'normal'
            emit('change-screen-size', currentScreenSize.value)
            window.localStorage.setItem('screenSize', currentScreenSize.value)
        }

        const iconType = computed(() => {
            return currentScreenSize.value === 'normal' ? 'maximize' : 'minimize'
        })

        return {
            currentOrientation,
            setOrientation,
            currentScreenSize,
            toggleScreenSize,
            iconType
        }
    }
}
</script>
