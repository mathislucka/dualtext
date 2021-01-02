<template>
    <div class="px-4 py-2 border-b border-grey-200 h-16"
        :class="{ 'ring-inset ring-2': hasFocus }">
        <input
            type="text"
            class="w-full :focus-outline-none outline-none h-full main-bg"
            placeholder="Search corpora..."
            :value="query"
            @keypress.stop="() => {}"
            @keydown.stop="() => {}"
            @input="$emit('update:query', $event.target.value)"
            @focus="focusParent"
            @blur="unfocusParent">
    </div>
</template>

<script>
export default {
  name: 'Search',
  emits: [ 'update:query' ],
  props: {
    query: {
        type: String,
        required: false,
        default: ''
    }
  },
  data () {
      return {
          hasFocus: false,
      }
  },
  methods: {
      focusParent () {
          this.hasFocus = true
      },
      unfocusParent () {
          this.hasFocus = false
      }
  },
}
</script>
