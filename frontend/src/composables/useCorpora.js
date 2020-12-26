import { onMounted, watch, computed } from 'vue'
import Corpus from './../store/Corpus.js'

const useCorpora = (project) => {
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

    onMounted(fetchProjectCorpora)
    watch(project, fetchProjectCorpora)

    return {
        corpora: computed(() => Object.values(Corpus.items.value))
    }
}

function useMultipleCorpora () {
    const fetchCorpora = () => {
        const isCached = Corpus.requests.value.find(request => request.type === 'list')

        if (!Corpus.isLoading.value && !isCached) {
            Corpus.actions.fetchCorpusList('/corpus/')
        }
    }

    onMounted(fetchCorpora)

    return {
        corpora: computed(() => Object.values(Corpus.items.value))
    }
}

export { useCorpora, useMultipleCorpora }