<template>
        <page-header />
        <two-column :fixedHeight="true">
            <template v-slot:left>
                <annotation-documents
                    :annotation="annotation"
                    :annotation-idx="annotationIdx" />
                <annotation-labels />
                <annotation-pager
                    :current-idx="annotationIdx + 1"
                    :next-annotation-id="nextAnnotationId"
                    :previous-annotation-id="previousAnnotationId"
                    :total-annotations="totalAnnotations" />
            </template>
            <template v-slot:right>
                <search-result-list :is-annotation-view="true" />
            </template>
        </two-column>
        <teleport to="#menu-content">
            <span v-for="task in openAnnotationTasks" :key="task.id">{{ task.name }}</span>
        </teleport>
</template>

<script>
import { toRefs, provide, computed } from 'vue'
import { useAnnotations } from './../../composables/useAnnotations.js'
import { useSingleProject } from './../../composables/useProjects.js'
import { useTask, useOpenTasks } from './../../composables/useTask.js'
import { useUser } from './../../composables/useUser.js'

import AnnotationPager from './AnnotationPager.vue'
import AnnotationDocuments from './AnnotationDocuments.vue'
import AnnotationLabels from './AnnotationLabels.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import SearchResultList from './../../components/shared/SearchResultList.vue'
import TwoColumn from './../../components/layout/TwoColumn.vue'
export default {
    name: 'AnnotationDetail',
    components: {
        AnnotationDocuments,
        AnnotationPager,
        AnnotationLabels,
        PageHeader,
        SearchResultList,
        TwoColumn
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

        const { user } = useUser()
        const userId = computed(() => user.value.id || '' )

        const { openAnnotationTasks, openReviewTasks } = useOpenTasks(userId, projectId)

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
            openAnnotationTasks,
            openReviewTasks,
            projectProvider,
            annotationProvider,
            taskProvider
        }
    }
}
</script>