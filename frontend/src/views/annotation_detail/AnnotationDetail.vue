<template>
        <page-header />
        <multi-column :columns="2">
            <card class="overflow-auto" :use-header="false">
                <template v-slot:content>
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
            </card>
            <card class="overflow-auto">
                <template v-slot:content>
                    <search-result-list :is-annotation-view="true" />
                </template>
            </card>
        </multi-column>
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
import MultiColumn from './../../components/layout/MultiColumn.vue'
import Card from './../../components/layout/Card.vue'
export default {
    name: 'AnnotationDetail',
    components: {
        AnnotationDocuments,
        AnnotationPager,
        AnnotationLabels,
        PageHeader,
        SearchResultList,
        MultiColumn,
        Card
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