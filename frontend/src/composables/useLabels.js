import { computed, watch, ref, onMounted } from 'vue'
import Label from './../store/Label.js'
import Annotation from './../store/Annotation.js'

function fetchProjectLabels (projectId) {
    projectId && Label.actions.fetchLabelList(`/project/${projectId}/label`)
}

function useLabels (project, annotation, userId, task) {
    function getAnnotatorLabels () {
        const ids = annotation.value.annotator_labels
        return ids.map(id => Label.items.value[id])
    }

    function getReviewerLabels () {
        const ids = annotation.value.reviewer_labels
        return ids.map(id => Label.items.value[id])
    }

    function removeLabel (labelId) {
        let labelPatch = { id: annotation.value.id }
        if (userId.value === task.value.annotator) {
            labelPatch.annotator_labels = annotation.value.annotator_labels.filter(label => label !== labelId)
        } else {
            labelPatch.reviewer_labels = annotation.value.reviewer_labels.filter(label => label !== labelId)
        }
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, labelPatch)
    }

    function addLabel (labelId) {
        let labelPatch = { id: annotation.value.id }
        if (userId.value === task.value.annotator) {
            labelPatch.annotator_labels = [ ...annotation.value.annotator_labels || [], labelId ]
        } else {
            labelPatch.reviewer_labels = [ ...annotation.value.reviewer_labels || [], labelId ]
        }
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, labelPatch)
    }

    const displayLabels = computed(() => {
        if (Object.keys(annotation.value).length === 0 || Label.isLoading.value) {
            return []
        }

        let userSensitiveLabels = []
        if (userId.value === task.value.annotator) {
            userSensitiveLabels = getAnnotatorLabels()
        } else {
            const reviewerLabels = getReviewerLabels()
            userSensitiveLabels = reviewerLabels.length > 0 ? reviewerLabels : getAnnotatorLabels()
        }
        return userSensitiveLabels
    })

    const availableLabels = computed(() => {
        return Label.isLoading.value ? [] : Object.values(Label.items.value)
    })

    watch(project, () => {
        fetchProjectLabels(project.value.id)
    })

    onMounted(() => {
        fetchProjectLabels(project.value.id)
    })

    return {
        addLabel,
        selectedLabels: displayLabels,
        availableLabels,
        removeLabel
    }
}

function useProjectLabels (projectId) {
    onMounted(() => {
        fetchProjectLabels(projectId.value)
    })

    watch(projectId, () => {
        fetchProjectLabels(projectId.value)
    })

    const labels = computed(() => Object.values(Label.items.value))

    return {
        labels
    }
}

export { useLabels, useProjectLabels }