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
                'add': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line>',
                'burger': '<line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line>',
                'chevron-down': '<polyline points="6 9 12 15 18 9"></polyline>',
                'chevron-left': '<polyline points="15 18 9 12 15 6"></polyline>',
                'chevron-right': '<polyline points="9 18 15 12 9 6"></polyline>',
                'close': '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>',
                'error': '<circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>',
                'plus': '<line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line>',
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