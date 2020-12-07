<template>
    <div>
        <span class="font-bold">Selected Labels</span>
        <div class="bg-grey-100 w-full p-4 minimum-height">
            <annotation-label
                @click="$emit('label-removed', label.id)"
                class="mr-2"
                v-for="label in selection" 
                :label="label"
                :key="label.id" />
        </div>
    </div>
</template>

<script>
import AnnotationLabel from './AnnotationLabel.vue'

export default {
    name: 'SelectedLabels',
    components: { AnnotationLabel },
    emits: [ 'label-removed' ],
    props: {
        selection: {
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