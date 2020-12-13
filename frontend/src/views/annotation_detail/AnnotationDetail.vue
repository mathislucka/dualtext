<template>
        <page-header />
        <main class="flex">
            <div class="ml-8 w-1/2 mt-4 mr-4 shadow mb-8">
                <annotation-documents
                    :annotation="annotation"
                    :annotation-idx="annotationIdx" />
                <annotation-labels />
                <annotation-pager
                    :current-idx="annotationIdx + 1"
                    :next-annotation-id="nextAnnotationId"
                    :previous-annotation-id="previousAnnotationId"
                    :total-annotations="totalAnnotations" />
            </div>
            <div class="w-1/2 mt-4 mr-8 ml-4 shadow mb-8 overflow-auto">
                <search-result-list class="overflow-auto" :is-annotation-view="true" />
            </div>
        </main>
</template>

<script>
import { toRefs, provide } from 'vue'
import { useAnnotations } from './../../composables/useAnnotations.js'
import { useSingleProject } from './../../composables/useProjects.js'
import { useTask } from './../../composables/useTask.js'

import AnnotationPager from './AnnotationPager.vue'
import AnnotationDocuments from './AnnotationDocuments.vue'
import AnnotationLabels from './AnnotationLabels.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import SearchResultList from './../../components/shared/SearchResultList.vue'
export default {
    name: 'AnnotationDetail',
    components: {
        AnnotationDocuments,
        AnnotationPager,
        AnnotationLabels,
        PageHeader,
        SearchResultList
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

        useSingleProject(projectId)
        useTask(taskId)

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