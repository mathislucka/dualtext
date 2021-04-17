<template>
    <div></div>
</template>

<script>
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { useAnnotationDecider } from './../../composables/useAnnotations.js'
import { useAnnotationGroupDecider } from './../../composables/useAnnotationGroups.js'
import { computed } from 'vue'

export default {
    name: 'AnnotationDecider',
    setup () {
        const route = useRoute()
        const { taskId, projectId } = route.params
        const isReview = computed(() => route.name === 'review_decider' || route.name === 'group_review_decider')
        const router = useRouter()
        const annotationRouteNames = [ 'review_decider', 'annotation_decider' ]
        const groupRouteNames = [ 'group_decider', 'group_review_decider' ]
        if (taskId && projectId && annotationRouteNames.includes(route.name)) {
            useAnnotationDecider(projectId, taskId, router, isReview)
        } else if (groupRouteNames.includes(route.name)) {
            useAnnotationGroupDecider(projectId, taskId, router, isReview)
        }
    },
}
</script>