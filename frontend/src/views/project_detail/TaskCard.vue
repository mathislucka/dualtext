<template>
    <card>
        <template v-slot:header>
            <div class="flex justify-between">
                <h2 class="font-semibold text-xl text-grey-800">{{ heading }}</h2>
                <button
                    :class="{ 'btn-primary': claimable > 0, 'btn-disabled': claimable === 0 }"
                    type="button"
                    @click="() => (claimable > 0 && claimTask())">Claim new ({{ claimable }})</button>
            </div>
        </template>
        <template v-slot:content>
            <div class="flex w-full">
                <div class="w-1/2">
                    <h3 class="text-lg font-semibold text-grey-600">Open</h3>
                    <ul>
                        <template v-for="task in openTasks" :key="task.id + 'open'">
                            <li class="mb-2 flex">
                                <router-link
                                    class="underline font-semibold text-blue-500 hover:text-blue-700 mr-4"
                                    :to="{ name: routeName, params: { projectId, taskId: task.id } }">
                                    {{ task.name }}
                                </router-link>
                                <button
                                    type="button"
                                    class="flex text-xs text-blue-500 hover:text-blue-700"
                                    title="unclaim"
                                    @click="unclaimTask(task.id)">
                                    <icon :icon="'user-x'" :height="16" :width="16" class="mt-1" />
                                </button>
                            </li>
                        </template>
                    </ul>
                </div>
                <div class="w-1/2">
                    <h3 class="text-lg font-semibold text-grey-600">Closed</h3>
                    <ul>
                        <template v-for="task in closedTasks" :key="task.id + 'closed'">
                            <li class="mb-2">
                                <router-link
                                    class="underline font-semibold text-blue-500 hover:text-blue-700"
                                    :to="{ name: routeName, params: { projectId, taskId: task.id } }">
                                    {{ task.name }}
                                </router-link>
                            </li>
                        </template>
                    </ul>
                </div>
            </div>
        </template>
    </card>
</template>

<script>
import { useOpenTasks, useClosedTasks, useTaskClaiming } from './../../composables/useTask.js'
import { useUser } from './../../composables/useUser.js'
import Card from './../../components/layout/Card.vue'
import Icon from './../../components/shared/Icon.vue'
import { computed, inject, toRefs } from 'vue'

export default {
    name: 'TaskCard',
    components: {
        Card,
        Icon
    },
    props: {
        taskType: {
            type: String,
            required: false,
            default: 'annotation'
        }
    },
    setup (props) {
        const { taskType } = toRefs(props)
        const projectId = inject('projectId')
    
        const { user } = useUser()
        const userId = computed(() => user.value.id || '' )

        const { openAnnotationTasks, openReviewTasks } = useOpenTasks(userId, projectId)
        const { closedAnnotationTasks, closedReviewTasks } = useClosedTasks(userId, projectId)

        const openTasks = taskType.value === 'annotation' ? openAnnotationTasks : openReviewTasks
        const closedTasks = taskType.value === 'annotation' ? closedAnnotationTasks : closedReviewTasks

        const {
            claimAnnotationTask,
            claimReviewTask,
            claimableTasks,
            unclaimAnnotationTask,
            unclaimReviewTask
        } = useTaskClaiming(projectId)

        const claimTask = taskType.value === 'annotation' ? claimAnnotationTask : claimReviewTask
        const claimable = computed(() => {
            return taskType.value === 'annotation'
                ? claimableTasks.value.open_annotations || 0
                : claimableTasks.value.open_reviews || 0
        })
        const unclaimTask = taskType.value === 'annotation' ? unclaimAnnotationTask : unclaimReviewTask

        const routeName = taskType.value === 'annotation' ? 'annotation_decider' : 'review_decider'

        const heading = computed(() => taskType.value === 'annotation' ? 'Annotation Tasks' : 'Review Tasks')
        return {
            claimable,
            claimTask,
            closedTasks,
            heading,
            openTasks,
            projectId,
            routeName,
            unclaimTask
        }
    }
}
</script>