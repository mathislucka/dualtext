<template>
    <div class="px-4 py-2 border-b border-grey-200 h-16"
        :class="{ 'ring-inset ring-2': hasFocus }">
        <input
            ref="search"
            type="text"
            class="w-full :focus-outline-none outline-none h-full main-bg"
            placeholder="Press '/' to search corpora..."
            @keypress.stop="() => {}"
            @keydown.stop="searchIfEnter($event)"
            v-model="currentQuery"
            @focus="focusParent"
            @blur="unfocusParent">
    </div>
</template>

<script>
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import { useSearch } from './../../composables/useSearch.js'
import Search from './../../store/Search.js'
import { ref, computed, inject, onMounted } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'Search',
  methods: {
      focusParent () {
          this.hasFocus = true
      },
      unfocusParent () {
          this.hasFocus = false
      },
      searchIfEnter (e) {
          if (e.code === 'Enter') {
            if (!this.shouldStayOnSearch) {
                this.$router.push({ name: 'explore_corpora', query: { ...this.currentFilters, query: this.currentQuery }})
            } else {
                this.runSearch()
                this.$router.push({ name: this.route.name, params: this.route.params, query: { ...this.currentFilters, query: this.currentQuery }})
            }
          }
      }
  },
  setup (props, context) {
    const route = useRoute()
    const shouldStayOnSearch = inject('shouldStayOnSearch', null)
    const search = ref(null)
    const hasFocus = ref(false)
    const focusSearch = (e) => {
        if (e.key === '/' || e.key === '+') {
            e.preventDefault()
            search.value && search.value.focus()
            hasFocus.value = true
        }
    }
    useGlobalEvents('keypress', focusSearch)

    const { query, setQuery, runSearch } = useSearch()

    const currentQuery = computed({
        get: () => query.value,
        set: (val) => {
            setQuery(val)
        }
    })
    const currentFilters = Search.selectedFilters

    onMounted(() => {
        if (route.query && Object.keys(route.query).length > 0) {
            const normalizedQuery = Object.entries(route.query).reduce((acc, [key, val]) => {
                if (key !== 'query') {
                    acc[key] = Array.isArray(val) ? val : [val]
                } else {
                    acc[key] = val
                }
                return acc
            },{})
            const {
                method,
                corpus,
                project,
                query
            } = normalizedQuery
            query && setQuery(query)
            Search.actions.setSelectedFilters({
                ...method ? { method: method } : {},
                ...corpus ? { corpus: corpus } : {},
                ...project ? { project: project } : {}
            })
            runSearch()
        }
    })

    return {
        search,
        hasFocus,
        currentQuery,
        runSearch,
        shouldStayOnSearch,
        currentFilters,
        route
    }
  }
}
</script>
