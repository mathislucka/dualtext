<template>
    <div></div>
</template>

<script>
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { useAnnotationDecider } from './../../composables/useAnnotations.js'
export default {
    name: 'AnnotationDecider',
    setup () {
        const { taskId, projectId } = useRoute().params
        const router = useRouter()
        if (taskId && projectId) {
            useAnnotationDecider(projectId, taskId, router)
        }
    },
}
</script>