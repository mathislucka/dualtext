<template>
    <div class="flex flex-col">
        
    </div>
</template>

<script>
import SearchResult from './SearchResult.vue'
export default {
    name: 'SearchResultList',
    components: {
        SearchResult
    },
    props: {
        isAnnotationView: {
            type: Boolean,
            required: false,
            default: false
        }
    },
    setup () {
        
    }
}
</script>