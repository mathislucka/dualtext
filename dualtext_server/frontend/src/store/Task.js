import { reactive, computed } from 'vue'
import { Api } from '../api/Api.js'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {},
    order: [],
    isLoading: false,
    requests: [],
    claimable: {},
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        async claim (path) {
            state.isLoading = true
            const response = await Api.patch(path)
            state.items[response.id] = response
            state.isLoading = false
        },
        fetchTask: actions.fetchResource,
        fetchTaskList: actions.fetchResourceList,
        updateTask: actions.updateResource,
        async fetchClaimableTasks (path) {
            state.isLoading = true
            const response = await Api.fetch(path)
            state.claimable = response
            state.isLoading = false
            return response
        }
    },
    claimable: computed(() => state.claimable),
    isLoading: computed(() => state.isLoading),
    items: computed(() => state.items),
    requests: computed(() => state.requests)
}
