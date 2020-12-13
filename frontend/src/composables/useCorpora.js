import { onMounted, watch, computed } from 'vue'
import Corpus from './../store/Corpus.js'

const useCorpora = (project) => {
    const fetchProjectCorpora = () => {
        console.log('project', project)
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

export { useCorpora }