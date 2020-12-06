import { computed, reactive } from 'vue'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {}
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchAnnotation: actions.fetchResource,
        fetchAnnotationList: actions.fetchResourceList,
        updateAnnotation: actions.updateResource
    },
    items: computed(() => state.items)
}
