<template>
    <div class="flex mr-4 mb-4 items-center">
        <div :style="swatchStyle" class="mr-2" />
        <div class="leading-4 text-sm">{{ swatch.key }}</div>
    </div>
</template>

<script>
export default {
    name: 'Swatch',
    props: {
        swatch: {
            type: Object,
            required: true
        }
    },
    computed: {
        swatchStyle () {
            return `background-color: ${this.swatch.color}; width: 16px; height: 16px;`
        }
    },
}
</script>