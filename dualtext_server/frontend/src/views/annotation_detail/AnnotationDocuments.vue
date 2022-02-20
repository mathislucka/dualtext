<template>
    <multi-column :columns="numColumns" class="p-0 w-full">
        <document 
            v-for="(document, idx) in documents"
            :key="idx"
            :document="document"
            :annotation-mode="annotationMode"
            @remove-document="removeDocument" />
    </multi-column>
</template>

<script>
import { toRefs, ref, computed, inject } from 'vue'
import { useDocuments } from './../../composables/useDocuments.js'
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import { useSingleProject } from './../../composables/useProjects.js'
import Search from './../../store/Search.js'
import Document from '../../components/shared/Document.vue'
import Annotation from './../../store/Annotation.js'
import MultiColumn from '../../components/layout/MultiColumn.vue'

export default {
    name: 'AnnotationDocuments',
    components: { Document, MultiColumn },
    props: {
        annotation: {
            type: Object,
            required: true
        },
        annotationIdx: {
            type: Number,
            required: true
        },
        orientation: {
            type: String,
            required: true
        }
    },
    setup (props) {
        const { annotation, annotationIdx, orientation } = toRefs(props)
        const taskId = inject('taskId')
        const projectId = inject('projectId')
        const isReview = inject('isReview')
        const { project } = useSingleProject(projectId)

        const {
            currentDocuments,
            removeDocument
        } = useDocuments(annotation, annotationIdx, taskId)

        const addDocumentToSearch = (e) => {
            if (e.key === '+' && currentDocuments.value.length > 0) {
                Search.actions.setSearchQuery(currentDocuments.value[0].content)
            }
        }

        useGlobalEvents('keypress', addDocumentToSearch)

        const annotationMode = computed(() => project.value.annotation_mode)

        const documents = computed(() => {
            const documents = currentDocuments.value
            while (documents.length < project.value.max_documents && annotationMode.value === 'dualtext' && !isReview.value) {
                documents.push({})
            }
            return documents
        })


        const numColumns = computed(() => orientation.value === 'vertical' ? documents.value.length : 1)

        return {
            documents,
            removeDocument,
            annotationMode,
            numColumns
        }
    }
}
</script>