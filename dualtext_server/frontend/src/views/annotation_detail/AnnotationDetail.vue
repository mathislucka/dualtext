<template>
        <page-header v-show="!isFullScreen" />
        <multi-column class="h-full" :columns="columnNumber" :class="{ 'p-0': isFullScreen }">
            <card class="overflow-auto relative h-full" :use-header="false">
                <template v-slot:content>
                    <div class="flex flex-col h-full">
                        <div class="grow">
                            <window-settings
                                v-if="!showSearch"
                                @share-link="setShareableLink"
                                :clipboard-message="clipboardMessage"
                                :shareable-link="shareableLink"
                                @change-orientation="setOrientation"
                                @change-screen-size="setScreenSize"/>
                            <desired-label v-if="!isReview && showSearch" :annotation="annotation" />
                            <annotation-documents
                                :annotation="annotation"
                                :annotation-idx="annotationIdx"
                                :orientation="currentOrientation" />
                        </div>
                        <div>
                            <annotation-labels
                                :is-review="isReview" />
                            <pager
                                class="mb-4"
                                :current-page="annotationIdx + 1"
                                :total-pages="totalAnnotations"
                                @page-down="handlePageDown"
                                @page-up="handlePageUp" />
                        </div>
                    </div>
                </template>
            </card>
            <card class="overflow-auto" v-if="showSearch" :use-header="false">
                <template v-slot:content>
                    <search-result-list :is-annotation-view="true" />
                </template>
            </card>
        </multi-column>
        <menu-content :project="project" />
</template>

<script>
import { provide, computed, ref, watch } from 'vue'
import { useAnnotations } from './../../composables/useAnnotations.js'
import { useSingleProject } from './../../composables/useProjects.js'
import { useTask } from './../../composables/useTask.js'
import { preparePageChangeHandler } from './../../composables/usePager.js'
import { useRoute, useRouter } from 'vue-router'

import Pager from './../../components/shared/Pager.vue'
import AnnotationDocuments from './AnnotationDocuments.vue'
import AnnotationLabels from './AnnotationLabels.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import SearchResultList from './../../components/shared/SearchResultList.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import Card from './../../components/layout/Card.vue'
import DesiredLabel from './DesiredLabel.vue'
import MenuContent from './../../components/shared/MenuContent.vue'
import WindowSettings from './WindowSettings.vue'

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
        DesiredLabel,
        MenuContent,
        WindowSettings
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

        const {
            nextAnnotationId,
            previousAnnotationId,
            totalAnnotations,
            annotation,
            annotations,
            annotationIdx,
        } = useAnnotations(taskId, annotationId)

        const currentOrientation = ref('horizontal')
        const setOrientation = (orientation) => {
            if (project.value.annotation_mode === 'classification' || isReview.value) {
                currentOrientation.value = orientation
            }
        }

        const currentScreenSize = ref('normal')
        const setScreenSize = (size) => {
            currentScreenSize.value = size
        }
        const isFullScreen = computed(() => {
            return currentScreenSize.value === 'full'
        })

        const shouldStayOnSearch = computed(() => !isReview.value && project.value.annotation_mode === 'dualtext')
        provide('shouldStayOnSearch', shouldStayOnSearch)
        const showSearch = computed(() => isReview.value === false && project.value.annotation_mode === 'dualtext')
        const columnNumber = computed(() => isReview.value || project.value.annotation_mode === 'classification' ? 1 : 2)

        const pageChangeParams = { projectId: projectId.value, taskId: taskId.value }
        const handlePageChange = preparePageChangeHandler(router, route.name, pageChangeParams)
        const handlePageDown = () => handlePageChange({ annotationId: previousAnnotationId.value })
        const handlePageUp = () => handlePageChange({ annotationId: nextAnnotationId.value })

        const shareableLink = ref('')
        const clipboardMessage = ref('')
        const setShareableLink = () => {
            shareableLink.value = `${window.location.protocol}//${window.location.host}/share/project/${projectId.value}/task/${taskId.value}/annotation/`
            navigator.clipboard.writeText(shareableLink.value).then(() => {
                clipboardMessage.value = 'link copied!'
                setTimeout(() => {
                    clipboardMessage.value = ''
                }, 2500)
            })
        }

        watch(annotationId, () => {
            shareableLink.value = ''
        })



        return {
            annotation,
            annotationIdx,
            columnNumber,
            isReview,
            nextAnnotationId,
            previousAnnotationId,
            totalAnnotations,
            project,
            showSearch,
            handlePageDown,
            handlePageUp,
            currentOrientation,
            setOrientation,
            setScreenSize,
            isFullScreen,
            setShareableLink,
            shareableLink,
            clipboardMessage
        }
    }
}
</script>