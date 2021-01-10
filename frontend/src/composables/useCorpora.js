import { onMounted, watch, computed } from 'vue'
import Corpus from './../store/Corpus.js'

const useCorpora = (project = {}) => {
    const fetchCorpora = () => {
        const isCached = Corpus.requests.value.find(request => request.type === 'list')

        if (!Corpus.isLoading.value && !isCached) {
            Corpus.actions.fetchCorpusList('/corpus/', {}, 'append')
        }
    }

    const fetchProjectCorpora = () => {
        if (project.value.corpora) {
            project.value.corpora.forEach(corpusId => fetchSingleCorpus(corpusId))
        }
    }

    const fetchSingleCorpus = (corpusId) => {
        if (!Corpus.items.value[corpusId]) {
            Corpus.actions.fetchCorpus(`/corpus/${corpusId}`)
        }
    }

    onMounted(()=> {
        if (project.value.id) {
            fetchProjectCorpora()
        } else {
            fetchCorpora()
        }
    })
    watch(project, () => {
        if (project.value.id) {
            fetchProjectCorpora()
        } else {
            fetchCorpora()
        }
    })

    const corpora = computed(() => {
        let out = Object.values(Corpus.items.value)
        if (project.value.id) {
            out = out.filter(corpus => project.value.corpora && project.value.corpora.includes(corpus.id))
        }
        return out
    })

    return {
        corpora
    }
}

function useSingleCorpus (corpusId) {
    const fetchCorpus = () => {
        if (!Corpus.items.value[corpusId.value]) {
            Corpus.actions.fetchCorpus(`/corpus/${corpusId.value}`)
        }
    }

    onMounted(fetchCorpus)
    watch(corpusId, fetchCorpus)

    const corpus = computed(() => Corpus.items.value[corpusId.value] || {})

    return {
        corpus
    }
}

export { useCorpora, useSingleCorpus }