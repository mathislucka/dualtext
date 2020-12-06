<template>
    <svg
        xmlns="http://www.w3.org/2000/svg"
        :width="width"
        :height="height"
        :viewBox="viewBox"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        v-html="iconContent">
    </svg>
</template>
<script>
export default {
    name: 'Icon',
    props: {
        height: {
            type: Number,
            required: false,
            default: 24
        },
        icon: {
            type: String,
            required: true
        },
        viewBox: {
            type: String,
            required: false,
            default: '0 0 24 24'
        },
        width: {
            type: Number,
            required: false,
            default: 24
        }
    },
    data () {
        return {
            icons: {
                'burger': '<line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line>',
                'chevron-down': '<polyline points="6 9 12 15 18 9"></polyline>',
                'chevron-left': '<polyline points="15 18 9 12 15 6"></polyline>',
                'chevron-right': '<polyline points="9 18 15 12 9 6"></polyline>',
                'close': '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>',
                'error': '<circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>'
            }
        }
    },
    computed: {
        iconContent () {
            return this.icons[this.icon]
        }
    }
}
</script>