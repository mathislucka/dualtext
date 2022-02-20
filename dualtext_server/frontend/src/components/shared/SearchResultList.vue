<template>
    <div>
        <loading v-if="isLoading" />
        <div v-if="!isLoading">
            <search-result
                :is-annotation-view="isAnnotationView"
                v-for="(result, idx) in results"
                :key="result.id"
                :result="result"
                :index="idx"
                class="block mb-4" />
        </div>
    </div>
</template>

<script>
import SearchResult from './SearchResult.vue'
import Search from './../../store/Search.js'
import { addDocument } from './../../composables/useDocuments.js'
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import Loading from './Loading.vue'
import { computed, onMounted, inject } from 'vue'
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
        const annotationId = inject('annotationId', null)
        onBeforeRouteUpdate((to, from) => {
            if (to.name === 'annotation_detail') {
                Search.actions.resetSearchResults()
            }
        })

        const results = computed(() => Search.results.value)
        if (annotationId) {
            const addDocumentByIdx = (e) => {
                if (e.key.match(/[0-9]/)) {
                    const document = results.value[parseInt(e.key)]
                    if (document && document.id) {
                        addDocument(document.id, annotationId)
                    }
                }
            }
            useGlobalEvents('keypress', addDocumentByIdx)
        }
        return {
            results,
            isLoading: computed(() => Search.isLoading.value)
        }
    }
}
</script>