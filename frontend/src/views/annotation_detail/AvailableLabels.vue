<template>
    <div>
        <span class="font-bold">Available Labels</span>
        <div class="w-full p-4 minimum-height bg-blue-100">
            <annotation-label
                @click="$emit('label-added', label.id)"
                class="mr-2"
                v-for="label in labels"
                :key="label.id"
                :label="label" />
        </div>
    </div>
</template>

<script>
import AnnotationLabel from './AnnotationLabel.vue'

export default {
    name: 'AvailableLabels',
    components: { AnnotationLabel },
    emits: [ 'label-added' ],
    props: {
        labels: {
            type: Object,
            required: true
        }
    }
}
</script>

<style scoped>
    .minimum-height {
        min-height: 4rem;
    }
</style>