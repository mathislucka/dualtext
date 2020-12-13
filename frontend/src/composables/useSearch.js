import { computed } from 'vue'
import Search from './../store/Search.js'
function useSearch () {
    function fetchSearchResults (corpora, methods, query) {
        Search.fetchSearchResults('/search/', { corpus: corpora, methods: methods, query: query })
    }

    return {
        fetchSearchResults,
        searchResults: computed(() => Search.results)
    }
}