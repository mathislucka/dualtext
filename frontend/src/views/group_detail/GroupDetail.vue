<template>
        <page-header />
        <multi-column :columns="columnNumber">
            <card class="overflow-auto" :use-header="false">
                <template v-slot:content>
                    <annotation
                        v-for="(annotation, idx) in currentAnnotationGroupAnnotations"
                        :key="annotation.id"
                        :annotation="annotation"
                        :project-id="projectId"
                        :annotation-idx="idx" />
                    <pager
                        :current-page="annotationGroupIdx + 1"
                        :total-pages="totalAnnotationGroups"
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
        <!-- <teleport to="#menu-content">
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
        </teleport> -->
</template>

<script>
import { toRefs, provide, computed, watch, ref } from 'vue'
import { useAnnotationGroups } from './../../composables/useAnnotationGroups.js'
import { useSingleProject } from './../../composables/useProjects.js'
import { useTask, useOpenTasks } from './../../composables/useTask.js'
import { preparePageChangeHandler } from './../../composables/usePager.js'
import { fetchGroupedDocuments } from './../../composables/useDocuments.js'
import { useUser } from './../../composables/useUser.js'
import { useRoute, useRouter } from 'vue-router'

import Annotation from './Annotation.vue'
import Pager from './../../components/shared/Pager.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import SearchResultList from './../../components/shared/SearchResultList.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import Card from './../../components/layout/Card.vue'

export default {
    name: 'AnnotationGroupDetail',
    components: {
        Annotation,
        Pager,
        PageHeader,
        SearchResultList,
        MultiColumn,
        Card,
    },
    props: {
        annotationGroupId: {
            type: Number,
            required: true
        },
        projectId: {
            type: Number,
            required: true
        },
        taskId: {
            type: Number,
            required: true
        }
    },
    setup (props, context) {
        const route = useRoute()
        const router = useRouter()
        const { annotationGroupId, projectId, taskId } = toRefs(props)
        const isReview = computed(() => route.name === 'group_review_detail')
        provide('projectId', projectId)
        provide('annotationGroupId', annotationGroupId)
        provide('taskId', taskId)
        provide('isReview', isReview)

        const { project } = useSingleProject(projectId)

        const corporaIds = computed(() => project.value.corpora || [])
        provide('corporaIds', corporaIds)

        useTask(taskId)

        const {
            annotationGroup,
            currentAnnotationGroupAnnotations,
            totalAnnotationGroups,
            annotationGroupIdx,
            nextAnnotationGroupId,
            previousAnnotationGroupId
        } = useAnnotationGroups(taskId, annotationGroupId)

        fetchGroupedDocuments(annotationGroupId, currentAnnotationGroupAnnotations, taskId)

        const currentAnnotationGroupAnnotationIds = computed(() => {
            return currentAnnotationGroupAnnotations.value.map(anno => anno.id)
        })

        provide('groupAnnotationIds', currentAnnotationGroupAnnotationIds)

        const columnNumber = computed(() => isReview.value ? 1 : 2)
        const shouldStayOnSearch = computed(() => !isReview.value)
        provide('shouldStayOnSearch', shouldStayOnSearch)
        const showSearch = computed(() => isReview.value === false)
        const pageChangeParams = { projectId: projectId.value, taskId: taskId.value }
        const handlePageChange = preparePageChangeHandler(router, route.name, pageChangeParams)
        const handlePageDown = () => handlePageChange({ annotationGroupId: previousAnnotationGroupId.value })
        const handlePageUp = () => handlePageChange({ annotationGroupId: nextAnnotationGroupId.value }) 

        return {
            currentAnnotationGroupAnnotations,
            annotationGroupIdx,
            columnNumber,
            isReview,
            totalAnnotationGroups,
            // openAnnotationTasks,
            // openReviewTasks,
            project,
            showSearch,
            handlePageDown,
            handlePageUp
        }
    }
}
</script>