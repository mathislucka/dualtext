<template>
    <main
        class="grid gap-8 p-8"
        :class="gridColClass">
        <slot />
    </main>
</template>

<script>
export default {
    name: 'MultiColumn',
    props: {
        columns: {
            type: Number,
            required: false,
            default: 3
        }
    },
    computed: {
      gridColClass () {
        const classes = [
              'grid-cols-1',
              'grid-cols-2',
              'grid-cols-3',
              'grid-cols-4'
        ]
        return classes[this.columns-1]
      }
    }
}
</script>