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
                    <annotation-pager
                        :is-review="isReview"
                        :current-idx="annotationIdx + 1"
                        :next-annotation-id="nextAnnotationId"
                        :previous-annotation-id="previousAnnotationId"
                        :total-annotations="totalAnnotations" />
                </template>
            </card>
            <card class="overflow-auto" v-if="isReview === false" :use-header="false">
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
import { useUser } from './../../composables/useUser.js'
import { useRoute, useRouter } from 'vue-router'

import AnnotationPager from './AnnotationPager.vue'
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
        AnnotationPager,
        AnnotationLabels,
        PageHeader,
        SearchResultList,
        MultiColumn,
        Card,
        DesiredLabel
    },
    setup (props, context) {
        const route = useRoute()

        const annotationId = computed(() => parseInt(route.params.annotationId || -1))
        const projectId = computed(() => parseInt(route.params.projectId || -1))
        const taskId = computed(() => parseInt(route.params.taskId || -1))
        const isReview = computed(() => route.name === 'review_detail')

        provide('projectId', projectId)
        provide('annotationId', annotationId)
        provide('taskId', taskId)
        provide('isReview', isReview)
        
        const { project } = useSingleProject(projectId)
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

        const columnNumber = computed(() => isReview.value ? 1 : 2)

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
            project
        }
    }
}
</script>