<template>
    <div class="flex justify-end mb-2">
    <div class="flex items-center justify-end bg-grey-100 rounded-sm py-1 px-2">
        <input
            :checked="isConfirmed"
            @input="confirmAnnotation"
            type="checkbox"
            id="confirm"
            class="mr-1" />
        <label for="confirm">reviewed</label>
    </div>
    </div>
</template>

<script>
import { computed, toRefs } from 'vue'
import Annotation from './../../store/Annotation.js'
export default {
    name: 'ReviewConfirmation',
    props: {
        annotation: {
            type: Object,
            required: true
        }
    },
    setup (props) {
        const { annotation } = toRefs(props)

        const isConfirmed = computed(() => !!annotation.value.is_reviewed)
        const confirmAnnotation = () => {
            Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, { id: annotation.value.id, is_reviewed: !isConfirmed.value})
        }

        return {
            isConfirmed,
            confirmAnnotation
        }
    }
}
</script>