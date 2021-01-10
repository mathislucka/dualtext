import Search from './../store/Search.js'
function useSearch () {
    return {
        query: Search.searchQuery,
        setQuery: Search.actions.setSearchQuery,
        runSearch: Search.actions.runSearch
    }
}

export { useSearch }