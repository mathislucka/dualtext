<template>
    <div class="mb-16">
        <div :class="{ 'mb-4': useMargin }">
            <span class="bg-blue-100 rounded-md px-2 py-1 mr-4" v-if="!isReview">{{ annotationIdx }}</span>
            <label-select
                :annotation="annotation"
                :project-id="projectId"
                :annotation-idx="annotationIdx" />
        </div>
        <document
            :class="{ 'mb-4': !document.content && idx < paddedDocuments.length - 1 }"
            v-for="(document, idx) in paddedDocuments"
            :key="document.id"
            :document="document"
            @remove-document="removeDocument" />
    </div>
</template>

<script>
import Project from './../../store/Project.js'
import { getAnnotationDocuments, prepareDocumentRemoval } from './../../composables/useDocuments.js'
import { computed, toRefs, inject } from 'vue'

import Document from './../../components/shared/Document.vue'
import LabelSelect from './LabelSelect.vue'

export default {
name: 'Annotation',
components: {
    Document,
    LabelSelect
},
props: {
    annotation: {
        type: Object,
        required: true
    },
    annotationIdx: {
        type: Number,
        required: true
    },
    projectId: {
        type: Number,
        required: true
    }
},
setup(props) {
    const { annotation, projectId } = toRefs(props)

    const { documents } = getAnnotationDocuments(annotation)
    const removeDocument = prepareDocumentRemoval(annotation)
    const project = computed(() => Project.items.value[projectId.value] || {})
    const isReview = inject('isReview')

    const paddedDocuments = computed(() => {
        const docs = [ ...documents.value ]
        const maxDocuments = project.value.max_documents || 0
        while (maxDocuments && docs.length < maxDocuments && !isReview.value) {
            docs.push({})
        }
        return docs
    })

    const useMargin = computed(() => {
        return !(paddedDocuments.value[0] && paddedDocuments.value[0].content)
    })

    return {
        paddedDocuments,
        removeDocument,
        isReview,
        useMargin
        // projectId,
        // annotation
    }
},
}
</script>