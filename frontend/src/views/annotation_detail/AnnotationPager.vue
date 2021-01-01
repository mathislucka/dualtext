<template>
    <div class="flex mt-4">
        <div class="w-1/12 flex justify-start items-center">
            <router-link
                v-if="previousAnnotationId > -1"
                :to="{ name: 'annotation_detail', params: { projectId, taskId, annotationId: previousAnnotationId }}"
                class="btn-icon">
                <icon :icon="'chevron-left'" />
            </router-link>
        </div>
        <div class="w-10/12 flex items-center justify-center">
            <span>{{ currentIdx + '/' + totalAnnotations }}</span>
        </div>
        <div class="w-1/12 flex justify-end items-center">
            <router-link
                v-if="nextAnnotationId > -1"
                :to="{ name: 'annotation_detail', params: { projectId, taskId, annotationId: nextAnnotationId }}"
                class="btn-icon">
                <icon :icon="'chevron-right'" />
            </router-link>
        </div>
    </div>
</template>

<script>
import Icon from '../../components/shared/Icon.vue'
import { inject } from 'vue'

export default {
    name: 'AnnotationPager',
    components: {
        Icon
    },
    props: {
        currentIdx: {
            type: Number,
            required: true
        },
        nextAnnotationId: {
            type: Number,
            required: true
        },
        previousAnnotationId: {
            type: Number,
            required: true
        },
        totalAnnotations: {
            type: Number,
            required: true
        }
    },
    setup () {
        const projectId = inject('projectId')
        const taskId = inject('taskId')

        return {
            projectId,
            taskId
        }
    }
}
</script>