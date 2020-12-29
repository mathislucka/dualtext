import { ref, onMounted, watch, computed } from 'vue'
import Annotation from './../store/Annotation.js'

const useAnnotations = (taskId, annoId) => {
    const annotations = computed(() => Object.values(Annotation.items.value))
    const annotationId = computed(() => {
        let id = annoId.value
        // if there is no annotationId select the first annotation without labels so that the annotator can pick up where they left off
        if (annoId.value === -1) {
            const firstOpenAnnotation = annotations.value.find(anno => anno.annotator_labels.length === 0)
            id = firstOpenAnnotation && firstOpenAnnotation.id || annotations.value[annotations.value.length -1] || -1
        }
        return id
    })
    console.log('annoId is', annoId.value)
    console.log('annotationId is', annotationId.value)
    const isAnnotationLoading = ref(false)
    const annotation = computed(() => annotationId.value === -1 ? {} : annotations.value.find(anno => anno.id === annotationId.value) || {})
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

    const fetchAnnotations = () => {
        isAnnotationLoading.value = true
        Annotation.actions.fetchAnnotationList(`/task/${taskId.value}/annotation/`)
            .then(() => {
                isAnnotationLoading.value = false
            })
    }

    const fetchAnnotation = () => {
        if (!Annotation.items.value[annotationId.value] && annotationId.value !== -1) {
            Annotation.actions.fetchAnnotation(`/annotation/${annotationId.value}`)
        }
    } 

    onMounted(fetchAnnotations)
    watch(taskId, fetchAnnotations)
    watch(annotationId, fetchAnnotation)

    return {
        annotation,
        annotations,
        isAnnotationLoading,
        annotationIdx,
        totalAnnotations,
        nextAnnotationId,
        previousAnnotationId,
        updateAnnotation: Annotation.actions.updateAnnotation
    }
}

export { useAnnotations }