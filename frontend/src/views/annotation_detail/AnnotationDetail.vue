<template>
    <div>
        <annotation-pager
            :current-idx="annotationIdx + 1"
            :next-annotation-id="nextAnnotationId"
            :previous-annotation-id="previousAnnotationId"
            :total-annotations="totalAnnotations" />
        <annotation-documents
            :annotation="annotation"
            :annotation-idx="annotationIdx" />
    </div>
</template>

<script>
import { toRefs, provide } from 'vue'
import { useAnnotations } from './../../composables/useAnnotations.js'
import AnnotationPager from './AnnotationPager.vue'
import AnnotationDocuments from './AnnotationDocuments.vue'

export default {
    name: 'AnnotationDetail',
    components: {
        AnnotationDocuments,
        AnnotationPager
    },
    props: {
        projectId: {
            type: Number,
            required: true
        },

        taskId: {
            type: Number,
            required: true
        },

        annotationId: {
            type: Number,
            required: true
        }
    },

    setup (props, context) {
        const { annotationId, taskId, projectId } = toRefs(props)
        const projectProvider = provide('projectId', projectId)
        const annotationProvider = provide('annotationId', annotationId)
        const taskProvider = provide('taskId', taskId)

        const {
            nextAnnotationId,
            previousAnnotationId,
            totalAnnotations,
            annotation,
            annotations,
            annotationIdx,
            isAnnotationLoading
        } = useAnnotations(taskId, annotationId)

        return {
            isAnnotationLoading,
            annotation,
            annotationIdx,
            nextAnnotationId,
            previousAnnotationId,
            totalAnnotations,
            projectProvider,
            annotationProvider,
            taskProvider
        }
    }
}
</script>