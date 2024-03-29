import { computed, onMounted, watch } from 'vue'
import Task from './../store/Task.js'

function fetchProjectTasks (projectId) {
    Task.actions.fetchTaskList(`/project/${projectId.value}/task/`)
}

function useTask (taskId) {
    const fetchTask = () => Task.actions.fetchTask(`/task/${taskId.value}`)
    const task = computed(() => {
        return getTask(taskId)
    })
    
    watch(taskId, () => {
        if (taskId.value && taskId.value > -1) {
            fetchTask(taskId.value)
        }
    })
    
    onMounted(() => {
        if (taskId.value && taskId.value > -1) {
            fetchTask(taskId.value)
        }
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
            .filter(task => task.annotator === userId.value && task.is_finished === false && task.action === 'annotate')
    })

    const openReviewTasks = computed(() => {
        return Object.values(Task.items.value)
            .filter(task => task.annotator === userId.value && task.is_finished === false && task.action === 'review')
    })

    watch(projectId, () => {
        if (projectId.value && projectId.value > -1) {
            fetchProjectTasks(projectId)
        }
    })

    onMounted(() => {
        if (projectId.value && projectId.value > -1) {
            fetchProjectTasks(projectId)
        }
    })

    return {
        openAnnotationTasks,
        openReviewTasks
    }
}

function useClosedTasks (userId, projectId) {
    const closedAnnotationTasks = computed(() => {
        return Object.values(Task.items.value)
            .filter(task => task.annotator === userId.value && task.is_finished === true && task.action === 'annotate')
    })

    const closedReviewTasks = computed(() => {
        return Object.values(Task.items.value)
            .filter(task => task.annotator === userId.value && task.is_finished === true && task.action === 'review')
    })

    watch(projectId, () => {
        if (projectId.value && projectId.value > -1) {
            fetchProjectTasks(projectId)
        }
    })

    onMounted(() => {
        if (projectId.value && projectId.value > -1) {
            fetchProjectTasks(projectId)
        }
    })

    return {
        closedAnnotationTasks,
        closedReviewTasks
    }
}

function useTaskClaiming(projectId) {
    const claimAnnotationTask = () => {
        Task.actions.claim(`/project/${projectId.value}/task/claim/annotation/`).then(() => fetchClaimableTasks())
    }

    const claimReviewTask = () => {
        Task.actions.claim(`/project/${projectId.value}/task/claim/review/`).then(() => fetchClaimableTasks())
    }

    const fetchClaimableTasks = () => {
        Task.actions.fetchClaimableTasks(`/project/${projectId.value}/task/claim/`)
    }

    const unclaimAnnotationTask = (taskId) => {
        Task.actions.updateTask(`/task/${taskId}`, { id: taskId, annotator: null }).then(() => fetchClaimableTasks())
    }

    const unclaimReviewTask = (taskId) => {
        Task.actions.updateTask(`/task/${taskId}`, { id: taskId, annotator: null }).then(() => fetchClaimableTasks())
    }

    onMounted(fetchClaimableTasks)
    watch(projectId, fetchClaimableTasks)

    return {
        claimAnnotationTask,
        claimReviewTask,
        claimableTasks: Task.claimable,
        unclaimAnnotationTask,
        unclaimReviewTask
    }
}

export { useTask, getTask, useOpenTasks, useClosedTasks, useTaskClaiming }

