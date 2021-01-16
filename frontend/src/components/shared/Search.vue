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
import { ref, computed, inject } from 'vue'

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
              e.preventDefault()
              this.runSearch()
            if (!this.shouldStayOnSearch) {
                this.$router.push({ name: 'explore_corpora' })
            }
          }
      }
  },
  setup (props, context) {
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

    return {
        search,
        hasFocus,
        currentQuery,
        runSearch,
        shouldStayOnSearch
    }
  }
}
</script>
