<template>
    <span
        @mouseenter="setLabelStyle('light')"
        @mouseleave="setLabelStyle('standard')"
        class="px-4 py-2 shadow text-black rounded-xl leading-4 centered cursor-pointer text-sm"
        :style="labelStyle">{{ label.name }}</span>
</template>

<script>
export default {
    name: 'AnnotationLabel',
    props: {
        label: {
            type: Object,
            required: true
        }
    },
    data () {
        return {
            labelStyle: { backgroundColor: this.label.color.standard }
        }
    },
    methods: {
        setLabelStyle (shade) {
            this.labelStyle.backgroundColor = this.label.color[shade]
        }
    }
}
</script>

<style scoped>
    .centered {
        text-align: center;
        position: relative;
        top: 50%;
        -ms-transform: translateY(-50%);
        -webkit-transform: translateY(-50%);
        transform: translateY(-50%);
    }
</style>