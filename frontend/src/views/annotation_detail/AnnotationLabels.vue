<template>
    <div class="w-full p-4 mt-8">
        <selected-labels
            @label-removed="removeLabel"
            class="mb-8"
            :selection='selectedLabels' />
        <available-labels
            @label-added="addLabel"
            :labels='availableLabels' />
    </div>
</template>

<script>
import { computed, inject, watch } from 'vue'
import Annotation from './../../store/Annotation.js'
import SelectedLabels from './SelectedLabels.vue'
import AvailableLabels from './AvailableLabels.vue'
import { UserStore } from './../../store/User.js'
import Project from '../../store/Project.js'
import { useLabels } from './../../composables/useLabels.js'
import { getTask } from './../../composables/useTask.js'

export default {
    name: 'AnnotationLabels',
    components: {
        AvailableLabels,
        SelectedLabels
    },
    setup () {
        const annotationId = inject('annotationId')
        const projectId = inject('projectId')
        const taskId = inject('taskId')
        
        const task = getTask(taskId)
        const project = computed(() => Project.items.value[projectId.value] || {})
        const annotation = computed(() => Annotation.items.value[annotationId.value] || {})
        const userId = computed(() => UserStore.user.value.id || '')
        const { addLabel, selectedLabels, availableLabels, removeLabel } = useLabels(project, annotation, userId, task)
        
        return {
            addLabel,
            selectedLabels,
            availableLabels: computed(() => {
                const selectedIds = selectedLabels.value.map(label => label && label.id)
                return availableLabels.value.filter(label => !selectedIds.includes(label && label.id))
            }),
            removeLabel
        }
    }
}
</script>