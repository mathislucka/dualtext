import { reactive, computed } from 'vue'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {}
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchDocument: actions.fetchResource,
        fetchDocumentList: actions.fetchResourceList,
        updateDocument: actions.updateResource
    },
    items: computed(() => state.items)
}
