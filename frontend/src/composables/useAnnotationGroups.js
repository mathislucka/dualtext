import { onMounted, watch, computed, ref } from 'vue'
import { useAnnotations } from './useAnnotations.js'
import AnnotationGroup from './../store/AnnotationGroup.js'

const fetchAnnotationGroups = (taskId) => {
    return AnnotationGroup.actions.fetchAnnotationGroupList(`/task/${taskId}/annotation-group/`, {})
}

const useAnnotationGroups = (taskId, annotationGroupId) => {
    const annotationGroups = computed(() => Object.values(AnnotationGroup.items.value).filter(group => group.task === taskId.value))
    const annotationGroup = computed(() => AnnotationGroup.items.value[annotationGroupId.value] || {})
    const annotationGroupIdx = computed(() => annotationGroups.value.findIndex(group => group.id === annotationGroupId.value))
    const totalAnnotationGroups = computed(() => annotationGroups.value.length)
    const nextAnnotationGroupId = computed(() => {
        let id = -1
        if (annotationGroupIdx.value > -1 && (totalAnnotationGroups.value -1 > annotationGroupIdx.value)) {
            id = annotationGroups.value[annotationGroupIdx.value + 1].id
        }
        return id
    })
    const previousAnnotationGroupId = computed(() => {
        let id = -1
        if (annotationGroupIdx.value > 0) {
            id = annotationGroups.value[annotationGroupIdx.value -1].id
        }
        return id
    })

    const { annotations, updateAnnotation } = useAnnotations(taskId, ref({}))

    const currentAnnotationGroupAnnotations = computed(() => {
        return annotations.value.filter(anno => anno.annotation_group === annotationGroupId.value)
    })

    const fetchAnnotationGroup = () => {
        if (!AnnotationGroup.items.value[annotationGroupId.value]) {
            AnnotationGroup.actions.fetchAnnotationGroup(`/annotation-group/${annotationGroupId.value}`)
        }
    } 

    onMounted(() => {
        fetchAnnotationGroups(taskId.value)
    })
    
    watch(taskId, () => {
        if (taskId.value && taskId.value > 1) {
            fetchAnnotationGroups(taskId.value)
        }
    })

    watch(annotationGroupId, () => {
        if (annotationGroupId.value && annotationGroupId.value > 1 && !AnnotationGroup.items.value[annotationGroupId.value]) {
            console.log(annotationGroups)
            console.log('called fetch')
            fetchAnnotationGroup()
        }
    })

    return {
        annotationGroup,
        annotationGroups,
        annotationGroupIdx,
        totalAnnotationGroups,
        nextAnnotationGroupId,
        previousAnnotationGroupId,
        updateAnnotation,
        currentAnnotationGroupAnnotations
    }
}

export { useAnnotationGroups }