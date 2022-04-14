<template>
    <div
        class="border-grey-700 rounded-sm"
        :class="{ 'border-2 border-dashed': !document.content }">
        <div
            v-if="document.content" class="p-4 relative text-2xl font-light subpixel-antialiased leading-9"
            @mouseup="handleTextWrap">
            <span v-html="document.content" />
            <button
                v-if="showRemoval"
                @click="$emit('remove-document', document.id)"
                class="absolute top-0 right-0 text-grey-400 hover:text-grey-700">
                <icon :icon="'close'" :width="16" :height="16" />
            </button>
        </div>
        <div v-if="!document.content" class="h-24 w-full"></div>
    </div>

</template>

<script>
import Icon from './Icon.vue'
import {computed, inject, toRefs} from 'vue'
export default {
    components: { Icon },
    name: 'document',
    emits: ['remove-document'],
    props: {
        document: {
            type: Object,
            required: false,
            default: () => ({})
        },
        annotationMode: {
            type: String,
            required: false,
            default: () => 'dualtext'
        }
    },
    setup (props) {
        const { annotationMode } = toRefs(props)
        const isReview = inject('isReview')
        const showRemoval = computed(() => {
            const currentMode = annotationMode && annotationMode.value || 'dualtext'
            return !isReview && currentMode
        })

        const handleTextWrap = (e) => {
            const selection = window.getSelection()
            if (selection.anchorOffset !== selection.focusOffset) {
                const span = document.createElement('span')
                span.setAttribute('class', 'radius-lg bg-yellow-200 highlight')
                span.setAttribute('title', 'Click to remove highlight.')
                const range = selection.getRangeAt(0).cloneRange()
                range.surroundContents(span)
                selection.removeAllRanges()
                selection.addRange(range)
            } else {
                const el = e.target
                if (el.classList.contains('highlight')) {
                    const parent = el.parentNode
                    while (el.firstChild) parent.insertBefore(el.firstChild, el)
                    parent.removeChild(el)
                }
            }
        }
        return {
            showRemoval,
            handleTextWrap
        }
    }
}
</script>