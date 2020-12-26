<template>
    <main class="flex">
        <div class="w-full ml-8 mr-8 mt-4 mb-8 shadow"
            :class="{ 'overflow-auto': fixedHeight }">
            <slot />
        </div>
    </main>
</template>

<script>
export default {
    name: 'SingleColumn',
    props: {
        fixedHeight: {
            type: Boolean,
            required: false,
            default: false
        }
    }
}
</script>