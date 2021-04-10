<template>
    <div class="flex mt-4">
        <div class="w-1/12 flex justify-start items-center">
            <a
                v-if="currentPage > minPage"
                href="#"
                @click.prevent="$emit('page-down')"
                class="btn-icon">
                <icon :icon="'chevron-left'" />
            </a>
        </div>
        <div class="w-10/12 flex items-center justify-center">
            <span>{{ currentPage + '/' + totalPages }}</span>
        </div>
        <div class="w-1/12 flex justify-end items-center">
            <a
                v-if="currentPage < totalPages"
                href="#"
                @click.prevent="$emit('page-up')"
                class="btn-icon">
                <icon :icon="'chevron-right'" />
            </a>
        </div>
    </div>
</template>

<script>
import Icon from './Icon.vue'
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import { toRefs } from 'vue'

export default {
    name: 'Pager',
    components: {
        Icon
    },
    emits: [ 'page-up', 'page-down' ],
    props: {
        currentPage: {
            type: Number,
            required: true
        },
        minPage: {
            type: Number,
            required: false,
            default: () => 1
        },
        totalPages: {
            type: Number,
            required: true
        }
    },
    setup (props, context) {
        const { currentPage, minPage, totalPages } = toRefs(props)

        const keyboardSwitch = (e) => {
            const key = e.key
            if (key === 'ArrowLeft' && currentPage.value > minPage.value) {
                context.emit('page-down')
            }

            if (key === 'ArrowRight' && currentPage.value < totalPages.value) {
                context.emit('page-up')
            }
        }

        useGlobalEvents('keydown', keyboardSwitch)
    }
}
</script>