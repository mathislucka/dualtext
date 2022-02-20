<template>
    <div class="flex shadow bg-grey-900 text-white mb-2 transition-opacity duration-700"
        :class="{'opacity-1': isMounted, 'opacity-0': !isMounted }">
        <div class="w-2/12 text-red-500 border-l-4 border-red-500 p-2 flex items-center justify-center"><icon :icon="iconName" /></div>
        <div class="w-9/12 p-2 text-xs">{{ notification.content }}</div>
        <div class="w-1/12 p-2 flex items-start justify-end hover:text-grey-300"><button @click="closeToast"><icon icon="close" :width="16" :height="16" /></button></div>
    </div>
</template>

<script>
import Icon from './Icon.vue'

export default {
    name: 'Toast',
    components: {
        Icon
    },
    props: {
        notification: {
            type: Object,
            required: true
        }
    },
    data () {
        return {
            isMounted: false
        }
    },
    computed: {
        iconName () {
            return this.notification.type === 'error' ? 'error' : 'exclamation'
        }
    },
    methods: {
        closeToast () {
            this.isMounted = false
            setTimeout(() => {
                this.$emit('close')
            }, 700)
        }
    },
    mounted () {
        setTimeout(() => {
            this.isMounted = true
        }, 100)
    }
}
</script>