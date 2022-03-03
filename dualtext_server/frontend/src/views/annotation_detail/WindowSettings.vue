<template>
    <div class="text-right">
        <transition>
            <div
                v-if="clipboardMessage !== ''"
                class="ml-auto mr-2 text-blue-500 text-sm align-middle p-1 mb-2 inline-block">
                    {{ clipboardMessage }}
            </div>
        </transition>
        <div
            v-if="shareableLink !== ''"
            class="ml-auto mr-2 text-blue-500 text-sm align-middle p-1 mb-2 inline-block">
            {{ shareableLink }}
        </div>
        <button
            v-if="showShare"
            @click="shareLink"
            title="get shareable link"
            class="btn-icon ml-auto mr-2 p-1">
            <icon icon="share" :height="16" :width="16" />
        </button>
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
import { computed, ref, toRefs } from 'vue'
import Icon from '../../components/shared/Icon.vue'

export default {
    name: 'WindowSettings',
    emits: [ 'change-orientation', 'change-screen-size', 'share-link' ],
    components: {
        Icon
    },
    props: {
        showShare: {
            type: Boolean,
            required: false,
            default: () => true
        },
        shareableLink: {
            type: String,
            required: false,
            default: () => ''
        },
        clipboardMessage: {
            type: String,
            required: false,
            default: () => ''
        }
    },
    setup (props, { emit }) {
        const { showShare, clipboardMessage, shareableLink } = toRefs(props)
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

        const shareLink = () => {
            emit('share-link')
        }

        return {
            currentOrientation,
            setOrientation,
            currentScreenSize,
            toggleScreenSize,
            iconType,
            showShare,
            clipboardMessage,
            shareableLink,
            shareLink
        }
    }
}
</script>
