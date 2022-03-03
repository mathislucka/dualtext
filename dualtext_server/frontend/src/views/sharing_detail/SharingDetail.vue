<template>
        <page-header v-if="!isFullScreen" />
        <multi-column class="h-full" :columns="1" :class="{ 'p-0': isFullScreen }">
            <card class="overflow-auto relative h-full" :use-header="false">
                <template v-slot:content>
                    <div class="flex flex-col h-full">
                        <div class="grow">
                            <window-settings
                                :show-share="false"
                                @change-orientation="setOrientation"
                                @change-screen-size="setScreenSize" />
                            <annotation-documents
                                :annotation="annotation"
                                annotation-idx="0"
                                :orientation="currentOrientation" />
                        </div>
                    </div>
                </template>
            </card>
        </multi-column>
</template>

<script>
import { provide, computed, ref } from 'vue'
import { useSingleAnnotation } from './../../composables/useAnnotations.js'
import { useRoute } from 'vue-router'

import AnnotationDocuments from './../annotation_detail/AnnotationDocuments.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import Card from './../../components/layout/Card.vue'
import WindowSettings from './../annotation_detail/WindowSettings.vue'
import {useSingleProject} from "../../composables/useProjects";

export default {
    name: 'SharingDetail',
    components: {
        AnnotationDocuments,
        PageHeader,
        MultiColumn,
        Card,
        WindowSettings
    },
    setup () {
        const route = useRoute()

        const annotationId = computed(() => parseInt(route.params.annotationId || -1))
        const projectId = computed(() => parseInt(route.params.projectId || -1))
        const taskId = computed(() => parseInt(route.params.taskId || -1))
        const isReview = ref(true)
        const { project } = useSingleProject(projectId)

        provide('projectId', projectId)
        provide('annotationId', annotationId)
        provide('isReview', isReview)
        provide('taskId', taskId)

        const {
            annotation
        } = useSingleAnnotation(annotationId)

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

        return {
            annotation,
            isReview,
            setOrientation,
            setScreenSize,
            currentOrientation,
            isFullScreen,
        }
    }
}
</script>