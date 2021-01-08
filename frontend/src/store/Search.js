import { reactive, computed } from 'vue'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {},
    order: [],
    isLoading: false,
    requests: [],
    searchQuery: null
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchSearchResult: actions.fetchResourceList,
        resetSearchResults: actions.resetStore,
        setSearchQuery (query) {
            state.searchQuery = query
        }
    },
    results: computed(() => state.order.map(id => state.items[id])),
    isLoading: computed(() => state.isLoading),
    requests: computed(() => state.requests),
    searchQuery: computed(() => state.searchQuery),
}
