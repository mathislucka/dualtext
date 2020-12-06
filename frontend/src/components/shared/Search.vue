<template>
    <div class="px-4 py-2 border-b border-grey-200 h-16"
        :class="{ 'ring-inset ring-2': hasFocus }">
        <input type="text" class="w-full :focus-outline-none outline-none h-full" placeholder="Search corpora..." @focus="focusParent" @blur="unfocusParent">
    </div>
</template>

<script>
export default {
  name: 'Search',
  props: {
    msg: String
  },
  data () {
      return {
          hasFocus: false
      }
  },
  methods: {
      focusParent () {
          this.hasFocus = true
      },
      unfocusParent () {
          this.hasFocus = false
      }
  }
}
</script>
