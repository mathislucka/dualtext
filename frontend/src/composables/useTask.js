import { computed, onMounted, watch } from 'vue'
import Task from './../store/Task.js'
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
    console.log('taskId', taskId)
    console.log('taskgetter', Task.items.value[taskId.value] || {})
    return computed(() => Task.items.value[taskId.value] || {})
}

export { useTask, getTask }

