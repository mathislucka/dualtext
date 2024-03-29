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
            <div class="w-full">
                <div class="w-full flex">
                    <button
                        class="p-2 border-b border-grey-300 rounded-t-md"
                        :class="openTabClass"
                        @click="setActiveTab('open')"
                        aria-label="Show open tasks.">
                        Open
                    </button>
                    <button
                        class="p-2 border-b border-grey-300 hover:border-blue-600  rounded-t-md"
                        :class="doneTabClass"
                        @click="setActiveTab('done')"
                        aria-label="Show closed tasks.">
                        Done
                    </button>
                    <div class="border-b border-grey-300 w-full"></div>
                </div>
                <table class="w-full">
                    <tbody>
                        <template v-for="task in activeTasks" :key="task.id + 'open'">
                            <tr class="border-b border-grey-100">
                                <td class="py-2">
                                    <router-link
                                        class="link mr-4"
                                        :to="{ name: routeName, params: { projectId, taskId: task.id } }">
                                        {{ task.name }}
                                    </router-link>
                                </td>
                                <td class="py-2">
                                    <label class="align-middle">
                                        <input type="checkbox" class="mr-2 align-middle" :checked="task.is_finished" @input="toggleTaskStatus(task)"/>
                                        <span class="align-middle">done</span>
                                    </label>
                                </td>
                                <td class="py-2">
                                    <button
                                        type="button"
                                        class="flex text-sm text-blue-500 hover:text-blue-700 hover:bg-grey-100 rounded-md p-2"
                                        title="unclaim task"
                                        @click="unclaimTask(task.id)">
                                        <icon :icon="'user-x'" :height="16" :width="16" class="mt-1 mr-2" />
                                        unclaim
                                    </button>
                                </td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>
        </template>
    </card>
</template>

<script>
import { useOpenTasks, useClosedTasks, useTaskClaiming } from './../../composables/useTask.js'
import { useUser } from './../../composables/useUser.js'
import Card from './../../components/layout/Card.vue'
import Icon from './../../components/shared/Icon.vue'
import Task from './../../store/Task.js'
import { computed, inject, toRefs, ref } from 'vue'

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
        const project = inject('project', ref(null))
    
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

        const routeName = computed(() => {
            const isAnnotationTask = taskType.value === 'annotation'
            const isGroup = project.value && project.value.annotation_mode === 'grouped'
            let routeName = 'annotation_decider'
            if (isAnnotationTask && !isGroup) {
                routeName = 'annotation_decider'
            }
            if (!isAnnotationTask && !isGroup) {
                routeName = 'review_decider'
            }
            if (isAnnotationTask && isGroup) {
                routeName = 'group_decider'
            }
            if (!isAnnotationTask && isGroup) {
                routeName = 'group_review_decider'
            }
            return routeName
        })

        const heading = computed(() => taskType.value === 'annotation' ? 'Annotation Tasks' : 'Review Tasks')

        const toggleTaskStatus = (task) => {
            Task.actions.updateTask(`/task/${task.id}`, { id: task.id, is_finished: !task.is_finished })
        }

        const tasks = computed(() => openTasks.value.concat(closedTasks.value))

        const activeTab = ref('open')

        const setActiveTab = (value) => {
            activeTab.value = value
        }

        const activeTasks = computed(() => {
            return activeTab.value == 'open' ? openTasks.value : closedTasks.value
        })

        const openTabClass = computed(() => {
            return activeTab.value == 'open' ? 'border-blue-600 text-blue-600 font-semibold' : 'hover:bg-grey-100'
        })
        const doneTabClass = computed(() => {
            return activeTab.value == 'done' ? 'border-blue-600 text-blue-600 font-semibold' : 'hover:bg-grey-100'
        })

        return {
            claimable,
            claimTask,
            heading,
            toggleTaskStatus,
            openTasks,
            closedTasks,
            projectId,
            routeName,
            unclaimTask,
            openTabClass,
            doneTabClass,
            activeTasks,
            setActiveTab
        }
    }
}
</script>