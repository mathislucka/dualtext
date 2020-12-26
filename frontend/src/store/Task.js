import { reactive, computed } from 'vue'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {},
    order: [],
    isLoading: false,
    requests: []
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchTask: actions.fetchResource,
        fetchTaskList: actions.fetchResourceList,
        updateTask: actions.updateResource
    },
    isLoading: computed(() => state.isLoading),
    items: computed(() => state.items),
    requests: computed(() => state.requests)
}
