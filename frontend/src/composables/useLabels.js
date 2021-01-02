import { computed, watch, onMounted, ref } from 'vue'
import Label from './../store/Label.js'
import Annotation from './../store/Annotation.js'
import { useGlobalEvents } from './useGlobalEvents.js'

function fetchProjectLabels (projectId) {
    projectId && Label.actions.fetchLabelList(`/project/${projectId}/label`)
}

function setReviewerLabels (annotation) {
    const reviewLabelPatch = { id: annotation.value.id, reviewer_labels: annotation.value.annotator_labels }
    Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, reviewLabelPatch)
}

function getAnnotatorLabels (annotation) {
    const ids = annotation.value.annotator_labels || []
    return ids.map(id => Label.items.value[id] || null).filter(label => label)
}

function getReviewerLabels (annotation) {
    const ids = annotation.value.reviewer_labels || []
    return ids.map(id => Label.items.value[id] || null).filter(label => label)
}

function useLabels (project, annotation, isReview = ref(false)) {
    function removeLabel (labelId) {
        let labelPatch = { id: annotation.value.id }
        if (isReview.value === true) {
            labelPatch.reviewer_labels = annotation.value.reviewer_labels.filter(label => label !== labelId)
        } else {
            labelPatch.annotator_labels = annotation.value.annotator_labels.filter(label => label !== labelId)
        }
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, labelPatch)
    }

    function addLabel (labelId) {
        let labelPatch = { id: annotation.value.id }
        if (isReview.value === true) {
            labelPatch.reviewer_labels = [ ...annotation.value.reviewer_labels || [], labelId ]
        } else {
            labelPatch.annotator_labels = [ ...annotation.value.annotator_labels || [], labelId ]
        }
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, labelPatch)
    }

    const annotatorLabels = computed(() => getAnnotatorLabels(annotation))

    const reviewerLabels = computed(() => getReviewerLabels(annotation))

    const availableLabels = computed(() => {
        return Object.values(Label.items.value)
    })

    const selectedLabels = computed(() => isReview.value === true ? reviewerLabels.value : annotatorLabels.value)

    const labelCallback = prepareLabelHotkeys(availableLabels, addLabel, removeLabel, selectedLabels)
    const unregister = useGlobalEvents('keypress', labelCallback)

    watch(project, () => {
        fetchProjectLabels(project.value.id)
    })

    const confirmAnnotatorLabels = () => {
        setReviewerLabels(annotation)
    }

    onMounted(() => {
        fetchProjectLabels(project.value.id)
    })

    return {
        addLabel,
        annotatorLabels,
        availableLabels,
        confirmAnnotatorLabels,
        removeLabel,
        reviewerLabels
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

function prepareLabelHotkeys (labels, addLabel, removeLabel, selectedLabels) {
    return function (event) {
        const keyMap = labels.value
            .filter(label => label)
            .reduce((acc, label) => {
                const keyCode = label.key_code
                if (keyCode) {
                    acc[keyCode] = label.id
                }
                return acc
            }, {})
        const labelId = keyMap[event.key]
        const isLabelSelected = selectedLabels.value.find(label => labelId === label.id)
        if (isLabelSelected && labelId) {
            removeLabel(labelId)
        } else if (labelId) {
            addLabel(labelId)
        }
    }
}

export { useLabels, useProjectLabels }