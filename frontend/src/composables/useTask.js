import { computed, onMounted, watch } from 'vue'
import Task from './../store/Task.js'

function fetchProjectTasks (projectId) {
    const isCached = Task.requests.value.find(request => request.type === 'list')
    if (!Task.isLoading.value && !isCached) {
        Task.actions.fetchTaskList(`/project/${projectId.value}/task/`)
    }
}

function useTask (taskId) {
    const fetchTask = () => Task.actions.fetchTask(`/task/${taskId.value}`)
    const task = computed(() => {
        return getTask(taskId)
    })
    
    watch(taskId, () => {
        fetchTask(taskId.value)
    })
    
    onMounted(() => {
        fetchTask(taskId.value)
    })

    return {
        task
    }
}

function getTask (taskId) {
    return computed(() => Task.items.value[taskId.value] || {})
}

function useOpenTasks (userId, projectId) {
    const openAnnotationTasks = computed(() => {
        return Object.values(Task.items.value)
            .filter(task => task.annotator === userId.value && task.is_annotated === false)
    })

    const openReviewTasks = computed(() => {
        return Object.values(Task.items.value)
            .filter(task => task.reviewer === userId.value && task.is_reviewed === false)
    })

    watch(projectId, () => {
        fetchProjectTasks(projectId)
    })

    onMounted(() => {
        fetchProjectTasks(projectId)
    })

    return {
        openAnnotationTasks,
        openReviewTasks
    }
}

export { useTask, getTask, useOpenTasks }

