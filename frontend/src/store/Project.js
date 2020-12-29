import { reactive, computed } from 'vue'
import { Api } from '../api/Api.js'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {},
    order: [],
    isLoading: false,
    requests: [],
    statistics: {}
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchProject: actions.fetchResource,
        fetchProjectList: actions.fetchResourceList,
        async fetchProjectStatistics (projectId) {
            state.isLoading = true
            const response = await Api.fetch(`/project/${projectId}/statistics`)
            state.statistics = response
            state.isLoading = false
            return response
        },
        updateProject: actions.updateResource
    },
    isLoading: computed(() => state.isLoading),
    items: computed(() => state.items),
    requests: computed(() => state.requests),
    statistics: computed(() => state.statistics)
}
