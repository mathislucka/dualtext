<template>
    <main
        class="grid gap-2 md:gap-8 md:p-8 auto-rows-auto grid-flow-rows pt-2"
        :class="`md:grid-cols-${columns}`">
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