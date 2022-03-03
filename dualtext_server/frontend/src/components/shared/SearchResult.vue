<template>
    <div class="flex flex-col">
        <div class="flex flex-row justify-start content-end">
            <button v-if="showSingleAddButtons" @click="addDocument(result.id)"><icon :icon="'plus'" class="text-grey-300 hover:text-grey-700 mr-1" :height="16" :width="16" /></button>
            <div class="relative mr-2"><span class="text-sm text-grey-500 text-center">method: {{ result.method }}</span></div>
            <button
                v-if="index <= 9 && showSingleAddButtons"
                class="shadow-sm rounded bg-grey-100 text-center text-xs py-1 px-2"
                @click="addDocument(result.id)">
                {{ index }}
            </button>
            <template v-for="(annoId, idx) in groupAnnotationIds" :key="annoId">
                <button
                    v-if="isAnnotationView"
                    class="bg-grey-100 text-center text-xs py-1 px-2 text-blue-500 shadow-sm rounded mr-2"
                    @click="addDocument(result.id, idx)">
                    {{ idx }}
                </button>
            </template>
        </div>
        <span>{{ result.content }}</span>
    </div>
</template>

<script>
import Icon from './Icon.vue'
import Annotation from './../../store/Annotation.js'
import Project from './../../store/Project.js'
import { inject, toRefs, computed, ref } from 'vue'

export default {
    name: 'SearchResult',
    components: {
        Icon
    },
    props: {
        result: {
            type: Object,
            required: true
        },
        isAnnotationView: {
            type: Boolean,
            required: false,
            default: false
        },
        index: {
            type: Number,
            required: false,
            default: 0
        }
    },
    setup (props) {
        const { isAnnotationView } = toRefs(props)
        const annotationId = inject('annotationId', null)
        const groupAnnotationIds = inject('groupAnnotationIds', ref([]))
        const projectId = inject('projectId')
        const project = computed(() => Project.items.value[projectId.value] || {})

        const addDocument = (docId, annotationIdx=null) => {
            const annotation = annotationIdx === null
                ? Annotation.items.value[annotationId.value]
                : Annotation.items.value[groupAnnotationIds.value[annotationIdx]]
            const max_documents = project.value.max_documents || 0
            if (annotation && annotation.documents) {
                const documents = annotation.documents.length === max_documents
                    ? [ ...annotation.documents.slice(0, max_documents - 1), docId ]
                    : [ ...annotation.documents, docId ]
                Annotation.actions.updateAnnotation(`/annotation/${annotation.id}`, { documents, id: annotation.id }, {})
            }
        }

        const showSingleAddButtons = computed(() => {
            return isAnnotationView.value && groupAnnotationIds.value.length === 0
        })

        return {
            addDocument,
            groupAnnotationIds,
            showSingleAddButtons
        }
    }
}
</script>