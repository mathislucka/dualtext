import { computed, watch, ref, onMounted } from 'vue'
import Label from './../store/Label.js'
import Annotation from './../store/Annotation.js'

function useLabels (project, annotation, userId, task) {
    const areLabelsLoading = ref(false)
    function fetchProjectLabels () {
        areLabelsLoading.value = true
        Label.actions.fetchLabelList(`/project/${project.value.id}/label`).then(() => {
            areLabelsLoading.value = false
        })
    }

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
            labelPatch.annotator_labels = [ ...annotation.value.annotator_labels, labelId ]
        } else {
            labelPatch.reviewer_labels = [ ...annotation.value.reviewer_labels, labelId ]
        }
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, labelPatch)
    }

    const displayLabels = computed(() => {
        if (areLabelsLoading.value || Object.keys(annotation.value).length === 0) {
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
        return Object.values(Label.items.value)
    })

    watch(project, () => {
        fetchProjectLabels()
    })

    onMounted(fetchProjectLabels)

    return {
        addLabel,
        selectedLabels: displayLabels,
        availableLabels,
        removeLabel
    }
}

export { useLabels }