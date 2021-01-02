<template>
    <div>
        <span class="font-bold">{{ heading }}</span>
        <div
            class="w-full px-4 pb-4 minimum-height flex flex-wrap"
            :class="backgroundColor">
            <annotation-label
                :uses-key="event !== ''"
                @click="clickEvent(label.id)"
                class="mr-2 mt-4"
                v-for="label in labels" 
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
    emits: [ 'label-removed', 'label-added' ],
    props: {
        labels: {
            type: Object,
            required: true
        },
        event: {
            type: String,
            required: false,
            default: ''
        },
        heading: {
        type: String,
        required: true
        },
        bgColor: {
            type: String,
            required: false,
            default: 'grey'
        }
    },
    computed: {
        clickEvent () {
            let callback = () => {}
            if (this.event !== '') {
                callback = (id) => {
                    this.$emit(this.event, id)
                }
            }
            return callback
        },
        backgroundColor () {
            return this.bgColor === 'grey' ? 'bg-grey-100' : 'bg-blue-100'
        }

    }
}
</script>
<style scoped>
    .minimum-height {
        min-height: 4rem;
    }
</style>