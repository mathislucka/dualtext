import { reactive, computed } from 'vue'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {},
    order: []
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchCorpus: actions.fetchResource,
        fetchCorpusList: actions.fetchResourceList,
        updateCorpus: actions.updateResource
    },
    items: computed(() => state.items)
}
