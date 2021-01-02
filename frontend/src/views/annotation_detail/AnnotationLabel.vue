<template>
    <button class="pl-4 shadow text-black rounded-xl leading-4 test-sm bg-grey-200">
        <div class="flex">
        <span class="pr-2 py-2">{{ label.key_code.toUpperCase() }}</span>
        <span
            @mouseenter="setLabelStyle('light')"
            @mouseleave="setLabelStyle('standard')"
            :class="labelInnerClass"
            :style="labelStyle">{{ label.name }}</span>
        </div>
    </button>
</template>

<script>
export default {
    name: 'AnnotationLabel',
    props: {
        label: {
            type: Object,
            required: true
        },
        usesKey: {
            type: Boolean,
            required: false,
            default: true
        }
    },
    data () {
        return {
            labelStyle: { backgroundColor: this.label.color.standard }
        }
    },
    computed: {
        labelInnerClass () {
            return this.usesKey ? 'py-2 pr-4 pl-2 rounded-r-xl' : 'px-4 py-2 shadow text-black rounded-xl leading-4 centered cursor-pointer text-sm'
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