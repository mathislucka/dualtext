<template>
    <main class="flex">
        <div class="ml-8 w-1/2 mt-4 mr-4 shadow mb-8 bg-white"
            :class="{ 'overflow-auto': fixedHeight }">
            <slot name="left" />
        </div>
        <div class="w-1/2 mt-4 mr-8 ml-4 shadow mb-8 bg-white"
            :class="{ 'overflow-auto': fixedHeight }">
            <slot name="right" />
        </div>
    </main>
</template>

<script>
export default {
    name: 'TwoColumn',
    props: {
        fixedHeight: {
            type: Boolean,
            required: false,
            default: false
        }
    }
}
</script>