import { computed, watch, onMounted, ref } from 'vue'
import Document from './../store/Document.js'
import Annotation from './../store/Annotation.js'

function useDocuments (annotation, currentAnnotationIdx, taskId) {
    const annotations = computed(() => Object.values(Annotation.items.value).filter(anno => anno.task === taskId.value))
    const areDocumentsLoading = ref(false)
    function getDocumentsForAnnotation (annotation) {
        const currentlyFetchingDocuments = []
        if (annotation.documents) {
            annotation.documents.forEach(docId => {
                if (!Document.items.value[docId]) {
                    currentlyFetchingDocuments.push(Document.actions.fetchDocument(`/document/${docId}`))
                }
            })
        }
        return currentlyFetchingDocuments
    }

    function fetchCurrentAndNextDocuments (annotation, numberOfAnnotations) {
        if (annotation.value && annotation.value.documents) {
            areDocumentsLoading.value = true
            const fetchingDocuments = getDocumentsForAnnotation(annotation.value)
            Promise.all(fetchingDocuments).then(() => {
                areDocumentsLoading.value = false
            })
        }
        if (annotations.value.length > 0) {
            const nextAnnotations = (annotations.value.length - 1) - currentAnnotationIdx.value
            const end = nextAnnotations > numberOfAnnotations ? currentAnnotationIdx.value + numberOfAnnotations : annotations.value.length - 1 
            const range = { start: currentAnnotationIdx.value + 1, end: end }
            for (let i = range.start; i <= range.end; i++) {
                getDocumentsForAnnotation(annotations.value[i])
            }
        }
    }

    function removeDocument (docId) {
        const documents = annotation.value.documents.filter(doc => doc !== docId)
        Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, { documents, id: annotation.value.id })
    }

    onMounted(() => {
        fetchCurrentAndNextDocuments(annotation, 10)
    })
    watch(annotation, () => {
        fetchCurrentAndNextDocuments(annotation, 10)
    })

    return {
        currentDocuments: computed(() => {
            const documents = []
            if(annotation.value.documents) {
                annotation.value.documents.forEach(docId => {
                    documents.push(Document.items.value[docId] || {})
                })
            }
            return documents
        }),
        removeDocument
    }
}

export { useDocuments }