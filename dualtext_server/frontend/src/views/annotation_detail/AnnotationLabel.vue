<template>
    <button
        class="shadow text-black rounded-xl leading-4 text-sm bg-grey-200"
        :class="{ 'pl-4': usesKey }">
        <div class="flex">
        <span class="pr-2 py-2" v-if="usesKey === true">{{ keyCode }}</span>
        <span
            @mouseenter="setLabelStyle('light')"
            @mouseleave="setLabelStyle('standard')"
            :class="labelInnerClass"
            :style="usedLabelStyle">{{ label.name }}</span>
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
        },
        usesLightColor: {
            type: Boolean,
            required: false,
            default: false
        }
    },
    data () {
        return {
            labelStyle: { backgroundColor: this.label.color.standard }
        }
    },
    computed: {
        labelInnerClass () {
            return this.usesKey ? 'py-2 pr-4 pl-2 rounded-r-xl' : 'px-4 py-2 rounded-xl'
        },
        usedLabelStyle () {
            return this.usesLightColor ? { backgroundColor: this.label.color.light } : this.labelStyle
        },
        keyCode () {
            return this.label.key_code.toUpperCase() === this.label.key_code
                ? `Shift + ${this.label.key_code}`
                : this.label.key_code.toUpperCase()
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