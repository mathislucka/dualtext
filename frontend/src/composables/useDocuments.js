import { computed, watch, onMounted, ref } from 'vue'
import Document from './../store/Document.js'
import Annotation from './../store/Annotation.js'
import AnnotationGroup from './../store/AnnotationGroup.js'

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

const prepareDocumentRemoval = (annotation) => (docId) => {
    const documents = annotation.value.documents.filter(doc => doc !== docId)
    Annotation.actions.updateAnnotation(`/annotation/${annotation.value.id}`, { documents, id: annotation.value.id })
}

function useDocuments (annotation, currentAnnotationIdx, taskId) {
    const annotations = computed(() => Object.values(Annotation.items.value).filter(anno => anno.task === taskId.value))
    const areDocumentsLoading = ref(false)

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

    const removeDocument = prepareDocumentRemoval(annotation)

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

function addDocument (docId, annotationId) {
    const annotation = Annotation.items.value[annotationId.value]
    if (annotation && annotation.documents) {
        const documents = annotation.documents.length === 2 ? [ annotation.documents[0], docId ] : [ ...annotation.documents, docId ]
        Annotation.actions.updateAnnotation(`/annotation/${annotation.id}`, { documents, id: annotation.id })
    }
}

function fetchCurrentAndNextGroupDocuments (groupId, nextGroupId) {
    const currentAnnotations = getGroupAnnotations(groupId)
    const nextAnnotations = nextGroupId !== -1 ? getGroupAnnotations(nextGroupId) : []
    const allAnnotations = [ ...currentAnnotations, ...nextAnnotations ]
    console.log('allannos', allAnnotations)
    allAnnotations.forEach(anno => getDocumentsForAnnotation(anno))
}

function getGroupAnnotations (groupId) {
    return Object.values(Annotation.items.value)
        .filter(anno => console.log(anno.annotation_group) || anno.annotation_group === groupId)
}

function fetchGroupedDocuments (groupId, annotations, taskId) {
    const nextGroupId = computed(() => {
        return Object.values(AnnotationGroup.items.value)
            .filter(g => g.task === taskId.value)
            .reduce((acc, curr, idx) => {
                return curr.id === groupId.value ? idx + 1 : acc
            }, -1)
    })

    onMounted(() => {
        console.log('called docs')
        fetchCurrentAndNextGroupDocuments(groupId.value, nextGroupId.value)
    })
    watch(groupId, () => {
        console.log('called docs id')
        fetchCurrentAndNextGroupDocuments(groupId.value, nextGroupId.value)
    })
    watch(annotations, () => {
        console.log('called docs anno')
        fetchCurrentAndNextGroupDocuments(groupId.value, nextGroupId.value)
    })
}

function getAnnotationDocuments (annotation) {
    const documents = computed(() => {
        return annotation.value.documents
            .map(id => Document.items.value[id] || null)
            .filter(doc => doc)
    })

    return {
        documents
    }
}

export { addDocument, useDocuments, fetchGroupedDocuments, prepareDocumentRemoval, getAnnotationDocuments }