<template>
    <div
        class="border-grey-700 rounded-sm"
        :class="{ 'border-2 border-dashed': !document.content }">
        <div v-if="document.content" class="p-4 relative text-2xl font-light">
            {{ document.content }}
            <button
                @click="$emit('remove-document', document.id)"
                class="absolute top-0 right-0 text-grey-400 hover:text-grey-700">
                <icon :icon="'close'" :width="16" :height="16" />
            </button>
        </div>
        <div v-if="!document.content" class="h-24 w-full"></div>
    </div>

</template>

<script>
import Icon from '../../components/shared/Icon.vue'
export default {
    components: { Icon },
    name: 'document',
    props: {
        document: {
            type: Object,
            required: false,
            default: () => ({})
        }
    }
}
</script>