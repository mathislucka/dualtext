<template>
    <card>
        <template v-slot:header>
            <h2 class="font-semibold text-xl text-grey-800">{{ corpus.name }}</h2>
        </template>
        <template v-slot:content>
            <div class="w-full flex flex-col">
                <pre class="bg-grey-100 p-4 mb-4">{{ JSON.stringify(corpus.corpus_meta, null, 4) }}</pre>
                <span class="font-semibold">This corpus contains {{ corpus.document_count }} documents.</span>
            </div>
        </template>
    </card>
</template>

<script>
import Card from '../../components/layout/Card.vue'
import { useSingleCorpus } from './../../composables/useCorpora.js'
import { toRefs } from 'vue'

export default {
    name: 'CorpusMetaCard',
    components: {
        Card,
    },
    props: {
        corpusId: {
            type: Number,
            required: true
        }
    },
    setup (props) {
        const { corpusId } = toRefs(props)
        const { corpus } = useSingleCorpus(corpusId)

        return {
            corpus
        }
        
    }
}
</script>