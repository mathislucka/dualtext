<template>
    <div class="h-full">
        <loading v-if="isLoading" />
        <div class="flex flex-col p-4" v-if="!isLoading">
            <search-result
                :is-annotation-view="isAnnotationView"
                v-for="result in results"
                :key="result.id"
                :result="result"
                class="mb-4" />
        </div>
    </div>
</template>

<script>
import SearchResult from './SearchResult.vue'
import Search from './../../store/Search.js'
import Loading from './Loading.vue'
import { computed } from 'vue'

export default {
    name: 'SearchResultList',
    components: {
        Loading,
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
        return {
            results: computed(() => Search.results.value),
            isLoading: computed(() => Search.isLoading.value)
        }
    }
}
</script>