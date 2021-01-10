<template>
    <div>
        <loading v-if="isLoading" />
        <div v-if="!isLoading">
            <search-result
                :is-annotation-view="isAnnotationView"
                v-for="result in results"
                :key="result.id"
                :result="result"
                class="block mb-4" />
        </div>
    </div>
</template>

<script>
import SearchResult from './SearchResult.vue'
import Search from './../../store/Search.js'
import Loading from './Loading.vue'
import { computed, onMounted } from 'vue'
import { onBeforeRouteUpdate } from 'vue-router'

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
        onBeforeRouteUpdate((to, from) => {
            if (to.name === 'annotation_detail') {
                Search.actions.resetSearchResults()
            }
        })
        return {
            results: computed(() => Search.results.value),
            isLoading: computed(() => Search.isLoading.value)
        }
    }
}
</script>