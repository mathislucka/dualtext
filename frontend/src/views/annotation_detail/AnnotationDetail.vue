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
import { toRefs, provide, computed, watch } from 'vue'
import { useAnnotations } from './../../composables/useAnnotations.js'
import { useSingleProject } from './../../composables/useProjects.js'
import { useTask, useOpenTasks } from './../../composables/useTask.js'
import { useUser } from './../../composables/useUser.js'
import { useRoute, useRouter } from 'vue-router'

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
    setup (props, context) {
        const route = useRoute()

        const annotationId = computed(() => parseInt(route.params.annotationId || -1))
        const projectId = computed(() => parseInt(route.params.projectId || -1))
        const taskId = computed(() => parseInt(route.params.taskId || -1))

        provide('projectId', projectId)
        provide('annotationId', annotationId)
        provide('taskId', taskId)
        if (projectId.value !== -1 && taskId.value !== -1 && annotationId.value !== -1) {
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
            } = useAnnotations(taskId, annotationId)

            return {
                annotation,
                annotationIdx,
                nextAnnotationId,
                previousAnnotationId,
                totalAnnotations,
                openAnnotationTasks,
                openReviewTasks,
            }
        } else {
            return {}
        }
    }
}
</script>