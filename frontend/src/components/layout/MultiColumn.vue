<template>
    <main
        class="grid gap-8 p-8"
        :class="`grid-cols-${columns}`">
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
    }
}
</script>