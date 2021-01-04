<template>
    <div class="flex justify-end mb-2">
    <div class="flex items-center justify-end rounded-sm py-4 px-4">
        <span class="text-grey-700 mr-2">Desired Label:</span>
        <annotation-label
            v-if="annotation.desired_label"
            :uses-key="false"
            :uses-light-color="true"
            :label="annotation.desired_label" />
    </div>
    </div>
</template>

<script>
import AnnotationLabel from './AnnotationLabel.vue'
export default {
    name: 'DesiredLabel',
    components: {
        AnnotationLabel
    },
    props: {
        annotation: {
            type: Object,
            required: true
        }
    },
}
</script>