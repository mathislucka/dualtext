<template>
        <page-header />
        <multi-column :columns="columnNumber">
            <card class="overflow-auto" :use-header="false">
                <template v-slot:content>
                    <desired-label v-if="!isReview" :annotation="annotation" />
                    <annotation-documents
                        :annotation="annotation"
                        :annotation-idx="annotationIdx" />
                    <annotation-labels
                        :is-review="isReview" />
                    <pager
                        :current-page="annotationIdx + 1"
                        :total-pages="totalAnnotations"
                        @page-down="handlePageDown"
                        @page-up="handlePageUp" />
                </template>
            </card>
            <card class="overflow-auto" v-if="showSearch" :use-header="false">
                <template v-slot:content>
                    <search-result-list :is-annotation-view="true" />
                </template>
            </card>
        </multi-column>
        <teleport to="#menu-content">
            <span class="font-semibold text-teal-500">Project</span>
            <router-link :to="{ name: 'project_detail', params: { projectId: project.id }}" class="link">{{ project.name }}</router-link>
            <span class="font-semibold text-teal-500 mt-4">Open Tasks</span>
            <router-link
                v-for="task in openAnnotationTasks"
                :key="task.id"
                class="link"
                :to="{ name: 'annotation_decider', params: { projectId: project.id, taskId: task.id }}">
                {{ task.name }}
            </router-link>
            <span class="font-semibold text-teal-500 mt-4">Open Reviews</span>
            <router-link
                v-for="task in openReviewTasks"
                :key="task.id"
                class="link"
                :to="{ name: 'review_decider', params: { projectId: project.id, taskId: task.id }}">
                {{ task.name }}
            </router-link>
        </teleport>
</template>

<script>
import { toRefs, provide, computed, watch } from 'vue'
import { useAnnotations } from './../../composables/useAnnotations.js'
import { useSingleProject } from './../../composables/useProjects.js'
import { useTask, useOpenTasks } from './../../composables/useTask.js'
import { preparePageChangeHandler } from './../../composables/usePager.js'
import { useUser } from './../../composables/useUser.js'
import { useRoute, useRouter } from 'vue-router'

import Pager from './../../components/shared/Pager.vue'
import AnnotationDocuments from './AnnotationDocuments.vue'
import AnnotationLabels from './AnnotationLabels.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import SearchResultList from './../../components/shared/SearchResultList.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import Card from './../../components/layout/Card.vue'
import DesiredLabel from './DesiredLabel.vue'

export default {
    name: 'AnnotationDetail',
    components: {
        AnnotationDocuments,
        Pager,
        AnnotationLabels,
        PageHeader,
        SearchResultList,
        MultiColumn,
        Card,
        DesiredLabel
    },
    setup (props, context) {
        const route = useRoute()
        const router = useRouter()

        const annotationId = computed(() => parseInt(route.params.annotationId || -1))
        const projectId = computed(() => parseInt(route.params.projectId || -1))
        const taskId = computed(() => parseInt(route.params.taskId || -1))
        const isReview = computed(() => route.name === 'review_detail')

        provide('projectId', projectId)
        provide('annotationId', annotationId)
        provide('taskId', taskId)
        provide('isReview', isReview)
        
        const { project } = useSingleProject(projectId)

        const corporaIds = computed(() => project.value.corpora || [])
        provide('corporaIds', corporaIds)

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

        const columnNumber = computed(() => isReview.value || project.value.annotation_mode === 'classification' ? 1 : 2)
        const shouldStayOnSearch = computed(() => !isReview.value && project.value.annotation_mode === 'dualtext')
        provide('shouldStayOnSearch', shouldStayOnSearch)
        const showSearch = computed(() => isReview.value === false && project.value.annotation_mode === 'dualtext')

        const pageChangeParams = { projectId: projectId.value, taskId: taskId.value }
        const handlePageChange = preparePageChangeHandler(router, route.name, pageChangeParams)
        const handlePageDown = () => handlePageChange({ annotationId: previousAnnotationId.value })
        const handlePageUp = () => handlePageChange({ annotationId: nextAnnotationId.value }) 

        return {
            annotation,
            annotationIdx,
            columnNumber,
            isReview,
            nextAnnotationId,
            previousAnnotationId,
            totalAnnotations,
            openAnnotationTasks,
            openReviewTasks,
            project,
            showSearch,
            handlePageDown,
            handlePageUp
        }
    }
}
</script>