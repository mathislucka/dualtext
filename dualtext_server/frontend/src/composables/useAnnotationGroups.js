import { onMounted, watch, computed, ref } from 'vue'
import { useAnnotations, fetchAnnotations } from './useAnnotations.js'
import { fetchProject } from './useProjects.js'
import AnnotationGroup from './../store/AnnotationGroup.js'
import Annotation from '../store/Annotation.js'
import Project from './../store/Project.js'

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

function navigateToNextGroup (projectId, router, taskId, routeName) {
    const groups = Object.values(AnnotationGroup.items.value)
    const annotations = Object.values(Annotation.items.value)
    const project = Project.items.value[projectId]
    const groupedAnnotations = groups.reduce((acc, current) => {
        const groupAnnotations = annotations.filter(anno => anno.annotation_group === current.id)
        acc.push(groupAnnotations)
        return acc
    }, [])
    let nextGroupId = groups.length !== 0 && groups[groups.length - 1].id
    let i = 0
    let isFound = false
    while (i < groupedAnnotations.length && !isFound) {
        isFound = groupedAnnotations[i].some(anno => anno.documents.length < project.max_documents || anno.labels.length === 0)
        if (isFound) {
            nextGroupId = groups[i].id
        }
        i++
    }
    console.log(nextGroupId)
    router.push({ name: routeName, params: { projectId: projectId, taskId: taskId, annotationGroupId: nextGroupId }})
}

function useAnnotationGroupDecider (projectId, taskId, router, isReview) {
    onMounted(() => {
        const routeName = isReview.value === true ? 'group_review_detail' : 'group_detail'
        const groupsAndAnnotationsFetched = [ fetchAnnotationGroups(taskId), fetchAnnotations(taskId),  fetchProject(projectId)]
        Promise.all(groupsAndAnnotationsFetched).then(() => {
            navigateToNextGroup(projectId, router, taskId, routeName)
        })
    })
}

export { useAnnotationGroups, useAnnotationGroupDecider }