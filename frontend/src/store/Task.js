import { reactive, computed } from 'vue'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {}
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchTask: actions.fetchResource,
        fetchTaskList: actions.fetchResourceList,
        updateTask: actions.updateResource
    },
    items: computed(() => state.items)
}
