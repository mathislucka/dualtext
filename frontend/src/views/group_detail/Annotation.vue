<template>
    <div class="mb-16">
        <div :class="{ 'mb-2': !firstDoc.content }">
            <span class="bg-blue-100 rounded-md px-2 py-1 mr-4">{{ annotationIdx }}</span>
            <label-select
                :annotation="annotation"
                :project-id="projectId" />
        </div>
        <document
            :document="firstDoc"
            @remove-document="removeDocument" />
    </div>
</template>

<script>
import { getAnnotationDocuments, prepareDocumentRemoval } from './../../composables/useDocuments.js'
import { computed, toRefs } from 'vue'

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
    const firstDoc = computed(() => documents.value[0] || {})

    return {
        firstDoc,
        removeDocument
        // projectId,
        // annotation
    }
},
}
</script>