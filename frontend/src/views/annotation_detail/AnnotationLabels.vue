<template>
    <div class="w-full md:mt-8 mt-2">
        <label-box
            class="mb-2"
            v-if="isReview"
            :labels="labelsToReview"
            :heading="'Annotator Labels'"
            :bg-color="'blue'" />
        <div
            v-if="isReview"
            class="flex justify-end">
            <button
                class="text-white px-2 py-1 hover:bg-blue-700 mb-4 bg-blue-500 shadow rounded"
                @click="confirmLabelsToReview">Confirm Labels (Space)</button>
        </div>
        <label-box
            :heading="'Selected Labels'"
            @label-removed="removeLabel"
            class="md:mb-8 mb-4"
            :labels="selectedLabels"
            :event="'label-removed'" />
        <label-box
            @label-added="addLabel"
            :heading="'Available Labels'"
            :labels="availableLabels"
            :bg-color="'blue'"
            :event="'label-added'" />
    </div>
</template>

<script>
import { computed, inject, watch, toRefs } from 'vue'
import Annotation from './../../store/Annotation.js'
import LabelBox from './LabelBox.vue'
import { UserStore } from './../../store/User.js'
import Project from '../../store/Project.js'
import { useLabels } from './../../composables/useLabels.js'
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import { getTask } from './../../composables/useTask.js'

export default {
    name: 'AnnotationLabels',
    components: {
        LabelBox
    },
    props: {
        isReview: {
            type: Boolean,
            required: true
        }
    },
    setup (props) {
        const { isReview } = toRefs(props)
        const annotationId = inject('annotationId')
        const projectId = inject('projectId')
        const project = computed(() => Project.items.value[projectId.value] || {})
        const annotation = computed(() => Annotation.items.value[annotationId.value] || {})

        const {
            addLabel,
            labels,
            availableLabels,
            confirmLabelsToReview,
            removeLabel,
            labelsToReview
        } = useLabels(project, annotation, isReview)

        if (isReview.value === true) {
            const confirmationCallback = (e) => {
                if (e.code === 'Space') {
                    confirmLabelsToReview()
                }
            }
            useGlobalEvents('keypress', confirmationCallback)
        }

        const selectedLabels = computed(() => labels.value)

        return {
            addLabel,
            selectedLabels,
            confirmLabelsToReview,
            availableLabels: computed(() => {
                const selectedIds = selectedLabels.value.map(label => label && label.id)
                return availableLabels.value.filter(label => !selectedIds.includes(label && label.id))
            }),
            removeLabel,
            labelsToReview
        }
    }
}
</script>