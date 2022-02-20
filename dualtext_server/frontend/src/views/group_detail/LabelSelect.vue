<template>
    <div class="inline">
        <label
            v-if="isReview"
            for="original-label"
            class="text-sm inline mr-2">
            Original label
        </label>
        <select
            id="original-label"
            v-if="isReview"
            class="text-sm mr-4"
            disabled
            :value="originalLabel">
            <option value="none">No label</option>
            <option
                v-for="option in options"
                :key="option.value"
                :value="option.value">
                {{ option.text }}
            </option>
        </select>
        <span v-if="isReview" class="mr-4">
            |
        </span>
        <label
            v-if="isReview"
            for="current-label"
            class="text-sm inline mr-2">
            Reviewer label
        </label>
        <select
            id="current-label"
            class="text-sm"
            :value="selectedLabel"
            @change="updateLabel">
            <option value="none">No label</option>
            <option
                v-for="option in options"
                :key="option.value"
                :value="option.value">
            {{ option.text }}
            </option>
        </select>
        <button
            v-if="isReview"
            class="text-white px-2 py-1 hover:bg-blue-700 mb-4 bg-blue-500 shadow rounded ml-4"
            @click="confirmLabelsToReview">
            Confirm (press {{ annotationIdx }})
        </button>
    </div>
</template>

<script>
import { useLabels } from './../../composables/useLabels.js'
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import { useSingleProject } from './../../composables/useProjects.js'
import { ref, computed, toRefs, inject } from 'vue'

export default {
    name: 'LabelSelect',
    props: {
        annotation: {
            type: Object,
            required: false,
            default: () => ({})
        },
        projectId: {
            type: Number,
            required: true
        },
        annotationIdx: {
            type: Number,
            required: true
        }
    },
    setup (props) {
        const { annotation, projectId, annotationIdx } = toRefs(props)
        const { project } = useSingleProject(projectId)
        const isReview = inject('isReview')
        const {
            availableLabels,
            labels,
            replaceLabel,
            removeAllLabels,
            labelsToReview,
            confirmLabelsToReview
        } = useLabels(project, annotation, ref(false), false)

        const labelOptions = computed(() => {
            return availableLabels.value.map(label => ({ value: label.id, text: label.name }))
        })

        const selectedLabel = computed(() => labels.value[0] && labels.value[0].id || 'none')
        const originalLabel = computed(() => labelsToReview.value[0] && labelsToReview.value[0].id || 'none')

        const updateLabel = (e) => {
            const labelValue = e.target.value
            if (labelValue !== 'none') {
                replaceLabel(labelValue)
            } else {
                removeAllLabels()
            }
        }

        const confirmLabelShortcut = (e) => {
            if (e.key == annotationIdx.value) {
                confirmLabelsToReview()
            }
        }

        useGlobalEvents('keypress', confirmLabelShortcut)

        return {
            options: labelOptions,
            updateLabel,
            selectedLabel,
            originalLabel,
            isReview,
            confirmLabelsToReview
        }
    }
}
</script>
