import { onMounted, watch, computed } from 'vue'
import Annotation from './../store/Annotation.js'

function fetchAnnotations (taskId) {
    return Annotation.actions.fetchAnnotationList(`/task/${taskId}/annotation/`)
}

const useAnnotations = (taskId, annotationId) => {
    const annotations = computed(() => Object.values(Annotation.items.value))
    const annotation = computed(() => Annotation.items.value[annotationId.value] || {})
    const annotationIdx = computed(() => annotations.value.findIndex(anno => anno.id === annotationId.value))
    const totalAnnotations = computed(() => annotations.value.length)
    const nextAnnotationId = computed(() => {
        let id = -1
        if (annotationIdx.value > -1 && ((annotations.value.length - 1) > annotationIdx.value)) {
            id = annotations.value[annotationIdx.value + 1].id
        }
        return id
    })
    const previousAnnotationId = computed(() => {
        let id = -1
        if (annotationIdx.value > 0) {
            id = annotations.value[annotationIdx.value -1].id
        }
        return id
    })

    const fetchAnnotation = () => {
        if (!Annotation.items.value[annotationId.value] && annotationId.value !== -1) {
            Annotation.actions.fetchAnnotation(`/annotation/${annotationId.value}`)
        }
    } 

    onMounted(() => {
        fetchAnnotations(taskId.value)
    })
    
    watch(taskId, () => {
        fetchAnnotations(taskId.value)
    })

    watch(annotationId, fetchAnnotation)

    return {
        annotation,
        annotations,
        annotationIdx,
        totalAnnotations,
        nextAnnotationId,
        previousAnnotationId,
        updateAnnotation: Annotation.actions.updateAnnotation
    }
}

function useAnnotationDecider (projectId, taskId, router, isReview) {
    const labelKey = isReview.value === true ? 'reviewer_labels' : 'annotator_labels'
    const routeName = isReview.value === true ? 'review_detail' : 'annotation_detail'
    onMounted(() => {
        fetchAnnotations(taskId).then(() => {
            const annotations = Object.values(Annotation.items.value)
            const nextOpenAnnotation = annotations.find(anno => anno[labelKey].length === 0) || annotations[annotations.length - 1]
            if (nextOpenAnnotation && nextOpenAnnotation.id) {
                router.push({ name: routeName, params: { projectId: projectId, taskId: taskId, annotationId: nextOpenAnnotation.id }})
            } else {
                router.push({ name: 'project_detail', params: { projectId: projectId }})
            }
        })
    })
}

export { useAnnotations, useAnnotationDecider }