<template>
  <select
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
</template>

<script>
import { useLabels } from './../../composables/useLabels.js'
import { useSingleProject } from './../../composables/useProjects.js'
import { ref, computed, toRefs } from 'vue'

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
        }
    },
    setup (props) {
        const { annotation, projectId } = toRefs(props)
        const { project } = useSingleProject(projectId)
        const {
            availableLabels,
            labels,
            replaceLabel,
            removeAllLabels
        } = useLabels(project, annotation, ref(false), false)

        const labelOptions = computed(() => {
            return availableLabels.value.map(label => ({ value: label.id, text: label.name }))
        })

        let selectedLabel = computed(() => labels.value[0] && labels.value[0].id || 'none')

        const updateLabel = (e) => {
            const labelValue = e.target.value
            console.log(labelValue)
            if (labelValue !== 'none') {
                replaceLabel(labelValue)
            } else {
                removeAllLabels()
            }
        }

        return {
            options: labelOptions,
            updateLabel,
            selectedLabel
        }
    }
}
</script>
