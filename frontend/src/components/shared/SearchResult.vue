<template>
    <div class="flex flex-col">
        <div class="flex flex-row justify-start">
            <button v-if="isAnnotationView"><icon :icon="add" /></button>
            <span class="text-sm text-grey-300">method: {{ result.method }}</span>
        <span>{{ result.content }}</span>
    </div>
</template>

<script>
import Icon from './Icon.vue'
export default {
    name: 'SearchResult',
    components: {
        Icon
    },
    props: {
        result: {
            type: Object,
            required: true
        },
        isAnnotationView: {
            type: Boolean,
            required: false,
            default: false
        }
    }
}
</script>