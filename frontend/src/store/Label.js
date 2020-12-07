import { reactive, computed } from 'vue'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {}
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchLabel: actions.fetchResource,
        fetchLabelList: actions.fetchResourceList,
        updateLabel: actions.updateResource
    },
    items: computed(() => state.items)
}
