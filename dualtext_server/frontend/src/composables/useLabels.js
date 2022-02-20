import { computed, watch, onMounted, ref } from 'vue'
import Label from './../store/Label.js'
import Annotation from './../store/Annotation.js'
import { useGlobalEvents } from './useGlobalEvents.js'

function fetchProjectLabels (projectId) {
    projectId && Label.actions.fetchLabelList(`/project/${projectId}/label`)
}

function setLabelsFromOrigin (annotation) {
    const origin = Annotation.items.value[annotation.value.copied_from]
    const reviewLabelPatch = { id: annotation.value.id, labels: origin.labels }
    Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, reviewLabelPatch)
}

function getAnnotatorLabels (annotation) {
    const ids = annotation.value.labels || []
    return ids.map(id => Label.items.value[id] || null).filter(label => label)
}

function useLabels (project, annotation, isReview = ref(false), useHotkeys = true) {
    function removeLabel (labelId) {
        let labelPatch = { id: annotation.value.id }
        labelPatch.labels = annotation.value.labels.filter(label => label !== labelId)
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, labelPatch)
    }

    function addLabel (labelId) {
        let labelPatch = { id: annotation.value.id }
        labelPatch.labels = [ ...annotation.value.labels || [], labelId ]
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, labelPatch)
    }

    function replaceLabel (labelId) {
        let labelPatch = { id: annotation.value.id, labels: [ labelId ] }
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, labelPatch)
    }

    function removeAllLabels () {
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, { id: annotation.value.id, labels: [] })
    }

    const labelsToReview = computed(() => {
        const reviewAnnotation = Annotation.items.value[annotation.value.copied_from]
        return reviewAnnotation && reviewAnnotation.labels.map(id => Label.items.value[id] || null).filter(label => label) || []
    })
    
    const labels = computed(() => getAnnotatorLabels(annotation) || [])

    const availableLabels = computed(() => {
        return Object.values(Label.items.value)
    })

    if (useHotkeys) {
        const labelCallback = prepareLabelHotkeys(availableLabels, addLabel, removeLabel, labels)
        const unregister = useGlobalEvents('keypress', labelCallback)
    }


    watch(project, () => {
        fetchProjectLabels(project.value.id)
    })

    const confirmLabelsToReview = () => {
        setLabelsFromOrigin(annotation)
    }

    onMounted(() => {
        fetchProjectLabels(project.value.id)
    })

    return {
        addLabel,
        labels,
        availableLabels,
        confirmLabelsToReview,
        removeLabel,
        replaceLabel,
        removeAllLabels,
        labelsToReview
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