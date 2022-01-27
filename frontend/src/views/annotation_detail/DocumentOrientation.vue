<template>
    <div class="text-right">
        <button
            @click="setOrientation('horizontal')"
            class="ml-auto mr-auto p-1 btn-icon"
            :class="{'btn-active': currentOrientation === 'horizontal' }">
            <icon icon="columns" height="16" width="16" class="rotate-90" />
        </button>
        <button
            @click="setOrientation('vertical')"
            class="ml-auto mr-auto p-1 btn-icon"
            :class="{'btn-active': currentOrientation === 'vertical' }">
            <icon icon="columns" height="16" width="16" />
        </button>
    </div>
</template>

<script>
import { ref } from 'vue'
import Icon from '../../components/shared/Icon.vue'

export default {
    name: 'DocumentOrientation',
    emits: [ 'orientation-change' ],
    components: {
        Icon
    },
    setup (_, { emit }) {
        const defaultOrientation = 'horizontal'
        const getOrientation = () => {
            const orientation = window.localStorage.getItem('orientation')
            emit('change-orientation', orientation || defaultOrientation)
            return orientation || defaultOrientation
        }

        const currentOrientation = ref(getOrientation())

        const setOrientation = (orientation) => {
            currentOrientation.value = orientation
            emit('change-orientation', currentOrientation.value)
            window.localStorage.setItem('orientation', currentOrientation.value)
        }

        return {
            currentOrientation,
            setOrientation
        }
    }
}
</script>
