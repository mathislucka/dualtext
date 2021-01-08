<template>
    <div></div>
</template>

<script>
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { useAnnotationDecider } from './../../composables/useAnnotations.js'
import { computed } from 'vue'
export default {
    name: 'AnnotationDecider',
    setup () {
        const route = useRoute()
        const { taskId, projectId } = route.params
        const isReview = computed(() => route.name === 'review_decider')
        const router = useRouter()
        console.log(taskId, projectId)
        if (taskId && projectId) {
            useAnnotationDecider(projectId, taskId, router, isReview)
        }
    },
}
</script>