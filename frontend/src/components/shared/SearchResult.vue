<template>
    <div class="flex flex-col">
        <div class="flex flex-row justify-start content-end">
            <button v-if="isAnnotationView" @click="addDocument(result.id)"><icon :icon="'add'" class="text-blue-300 hover:text-blue-600 mr-1" /></button>
            <div class="relative w-full"><span class="text-sm text-grey-500 absolute -bottom-1">method: {{ result.method }}</span></div>
        </div>
        <span>{{ result.content }}</span>
    </div>
</template>

<script>
import Icon from './Icon.vue'
import Annotation from './../../store/Annotation.js'
import { inject } from 'vue'

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
    },
    setup (props) {
        const annotationId = inject('annotationId')

        const addDocument = (docId) => {
            const annotation = Annotation.items.value[annotationId.value]
            if (annotation && annotation.documents) {
                const documents = annotation.documents.length === 2 ? [ annotation.documents[0], docId ] : [ ...annotation.documents, docId ]
                Annotation.actions.updateAnnotation(`/annotation/${annotation.id}`, { documents, id: annotation.id })
            }
        }

        return {
            addDocument
        }
    }
}
</script>