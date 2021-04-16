<template>
    <div>
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
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import { useSingleProject } from './../../composables/useProjects.js'
import Search from './../../store/Search.js'
import Document from '../../components/shared/Document.vue'
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
        const projectId = inject('projectId')
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



        return {
            documents: computed(() => {
                const documents = currentDocuments.value
                while (documents.length < 2 && project.value.annotation_mode === 'dualtext') {
                    documents.push({})
                }
                return documents
            }),
            removeDocument
        }
    }
}
</script>