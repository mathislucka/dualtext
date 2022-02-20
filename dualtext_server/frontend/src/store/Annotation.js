import { computed, reactive } from 'vue'
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
        fetchAnnotation: actions.fetchResource,
        fetchAnnotationList: actions.fetchResourceList,
        updateAnnotation: actions.updateResource
    },
    isLoading: computed(() => state.isLoading),
    items: computed(() => state.items),
    requests: computed(() => state.requests)
}
