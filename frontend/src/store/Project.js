import { reactive, computed } from 'vue'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {},
    order: []
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchProject: actions.fetchResource,
        fetchProjectList: actions.fetchResourceList,
        updateProject: actions.updateResource
    },
    items: computed(() => state.items)
}
