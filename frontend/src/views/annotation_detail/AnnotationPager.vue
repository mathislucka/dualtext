<template>
    <div class="flex mt-4">
        <div class="w-1/12 flex justify-start items-center">
            <router-link
                v-if="previousAnnotationId > -1"
                :to="{ name: routeName, params: { projectId, taskId, annotationId: previousAnnotationId }}"
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
                :to="{ name: routeName, params: { projectId, taskId, annotationId: nextAnnotationId }}"
                class="btn-icon">
                <icon :icon="'chevron-right'" />
            </router-link>
        </div>
    </div>
</template>

<script>
import Icon from '../../components/shared/Icon.vue'
import { useGlobalEvents } from './../../composables/useGlobalEvents.js'
import { inject, toRefs, computed } from 'vue'
import { useRouter } from 'vue-router'

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
        isReview: {
            type: Boolean,
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
    setup (props) {
        const { isReview, nextAnnotationId, previousAnnotationId } = toRefs(props)
        const projectId = inject('projectId')
        const taskId = inject('taskId')
        const routeName = computed(() => isReview.value === true ? 'review_detail' : 'annotation_detail')
        const router = useRouter()

        const keyboardSwitch = (e) => {
            console.log(e)
            const key = e.key
            if (key === 'ArrowLeft' && previousAnnotationId.value > -1) {
                router.push({
                    name: routeName.value,
                    params: { projectId: projectId.value, taskId: taskId.value, annotationId: previousAnnotationId.value }
                })
            }

            if (key === 'ArrowRight' && nextAnnotationId.value > -1) {
                router.push({
                    name: routeName.value,
                    params: { projectId: projectId.value, taskId: taskId.value, annotationId: nextAnnotationId.value }
                })
            }
        }

        useGlobalEvents('keydown', keyboardSwitch)
        return {
            projectId,
            taskId,
            routeName
        }
    }
}
</script>