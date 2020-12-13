<template>
    <div class="p-4">
        <document 
            v-for="(document, idx) in documents"
            :key="idx"
            :document="document"
            :class="{ 'mb-16': idx !== documents.length - 1}"
            @remove-document="removeDocument" />
    </div>
</template>

<script>
import { toRefs, ref, computed, inject } from 'vue'
import { useDocuments } from './../../composables/useDocuments.js'
import Document from './Document.vue'
import Annotation from './../../store/Annotation.js'
export default {
    name: 'AnnotationDocuments',
    components: { Document },
    props: {
        annotation: {
            type: Object,
            required: true
        },
        annotationIdx: {
            type: Number,
            required: true
        }
    },
    setup (props) {
        const { annotation, annotationIdx } = toRefs(props)
        const taskId = inject('taskId')

        const {
            currentDocuments,
            removeDocument
        } = useDocuments(annotation, annotationIdx)

        return {
            documents: computed(() => {
                const documents = currentDocuments.value
                while (documents.length < 2) {
                    documents.push({})
                }
                return documents
            }),
            removeDocument
        }
    }
}
</script>