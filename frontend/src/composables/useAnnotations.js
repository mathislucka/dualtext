import { ref, onMounted, watch, computed } from 'vue'
import Annotation from './../store/Annotation.js'

const useAnnotations = (taskId, annotationId) => {
    const isAnnotationLoading = ref(false)
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

    const fetchAnnotations = () => {
        if (Object.keys(annotation.value).length === 0) {
            isAnnotationLoading.value = true
            Annotation.actions.fetchAnnotationList(`/task/${taskId.value}/annotation`)
                .then(() => {
                    console.log(Annotation.items)
                    isAnnotationLoading.value = false
                })
        }
    }

    onMounted(fetchAnnotations)
    watch(annotationId, fetchAnnotations)

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