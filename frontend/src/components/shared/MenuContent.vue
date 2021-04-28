<template>
    <teleport to="#menu-content">
        <span class="font-semibold text-teal-500">Project</span>
        <router-link :to="{ name: 'project_detail', params: { projectId: project.id }}" class="link">{{ project.name }}</router-link>
        <span class="font-semibold text-teal-500 mt-4">Open Tasks</span>
        <router-link
            v-for="task in openAnnotationTasks"
            :key="task.id"
            class="link"
            :to="{ name: annotationRouteName, params: { projectId: project.id, taskId: task.id }}">
            {{ task.name }}
        </router-link>
        <span class="font-semibold text-teal-500 mt-4">Open Reviews</span>
        <router-link
            v-for="task in openReviewTasks"
            :key="task.id"
            class="link"
            :to="{ name: reviewRouteName, params: { projectId: project.id, taskId: task.id }}">
            {{ task.name }}
        </router-link>
    </teleport>
</template>
<script>
import { useUser } from './../../composables/useUser.js'
import { useOpenTasks } from './../../composables/useTask.js'
import { computed, ref, toRefs } from 'vue'

export default {
    name: 'MenuContent',
    props: {
        project: {
            type: Object,
            required: true
        },
        isGroup: {
            type: Boolean,
            required: false,
            default: false
        }
    },
    setup (props) {
        const { isGroup, project } = toRefs(props)
        const { user } = useUser()
        const userId = computed(() => user.value.id || '' )

        const { openAnnotationTasks, openReviewTasks } = useOpenTasks(userId, ref(project.value.id))
        const reviewRouteName = computed(() => isGroup.value ? 'group_review_decider' : 'review_decider')
        const annotationRouteName = computed(() => isGroup.value ? 'group_decider' : 'annotation_decider')

        return {
            openReviewTasks,
            openAnnotationTasks,
            annotationRouteName,
            reviewRouteName
        }
    }
}
</script>