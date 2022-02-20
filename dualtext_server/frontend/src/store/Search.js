import { reactive, computed } from 'vue'
import { Api } from './../api/Api.js'
import { initDefaultStoreMethods } from './DefaultStore.js'

let state = reactive({
    items: {},
    order: [],
    isLoading: false,
    requests: [],
    searchQuery: null,
    selectedFilters: {},
    availableMethods: []
})

const { actions } = initDefaultStoreMethods(state)

export default {
    actions: {
        fetchSearchResult: actions.fetchResourceList,
        resetSearchResults: actions.resetStore,
        setSearchQuery (query) {
            state.searchQuery = query
        },
        setSelectedFilters (filters) {
            state.selectedFilters = filters
        },
        runSearch () {
            actions.fetchResourceList('/search/', { ...state.selectedFilters, query: state.searchQuery })
        },
        async fetchSearchMethods () {
            const response = await Api.fetch('/search/methods')
            state.availableMethods = response
        }
    },
    availableMethods: computed(() => state.availableMethods),
    results: computed(() => state.order.map(id => state.items[id])),
    isLoading: computed(() => state.isLoading),
    requests: computed(() => state.requests),
    searchQuery: computed(() => state.searchQuery),
    selectedFilters: computed(() => state.selectedFilters)
}
