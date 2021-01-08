import { ref, watch } from 'vue'
import Search from './../store/Search.js'
function useSearch () {
    const query = ref('')
    watch(Search.searchQuery, () => {
        if (Search.searchQuery.value) {
            query.value = Search.searchQuery.value
        }
    })

    return {
        query
    }
}

export { useSearch }