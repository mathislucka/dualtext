<template>
    <div class="px-4 py-2 border-b border-grey-200 h-16"
        :class="{ 'ring-inset ring-2': hasFocus }">
        <input
            ref="search"
            type="text"
            class="w-full :focus-outline-none outline-none h-full main-bg"
            placeholder="Press '/' to search corpora..."
            :value="query"
            @keypress.stop="() => {}"
            @keydown.stop="bubbleEnter($event)"
            @input="$emit('update:query', $event.target.value)"
            @focus="focusParent"
            @blur="unfocusParent">
    </div>
</template>

<script>
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import { ref } from 'vue'

export default {
  name: 'Search',
  emits: [ 'update:query', 'keydown' ],
  props: {
    query: {
        type: String,
        required: false,
        default: ''
    }
  },
  methods: {
      focusParent () {
          this.hasFocus = true
      },
      unfocusParent () {
          this.hasFocus = false
      },
      bubbleEnter (e) {
          if (e.code === 'Enter') {
              this.$emit('keydown', e)
          }
      }
  },
  setup () {
      const search = ref(null)
        const hasFocus = ref(false)
      const focusSearch = (e) => {
          if (e.key === '/') {
            e.preventDefault()
            search.value && search.value.focus()
            hasFocus.value = true
          }
      }
      useGlobalEvents('keypress', focusSearch)

      return {
          search,
          hasFocus
      }
  }
}
</script>
