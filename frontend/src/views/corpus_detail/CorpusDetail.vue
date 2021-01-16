<template>
        <page-header />
        <multi-column :columns="2">
            <corpus-meta-card :corpus-id="corpusId" />
            <card class="overflow-auto" :use-header="false">
                <template v-slot:content>
                    <search-result-list />
                </template>
            </card>
        </multi-column>
</template>

<script>
import PageHeader from './../../components/shared/PageHeader.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import CorpusMetaCard from './CorpusMetaCard.vue'
import SearchResultList from './../../components/shared/SearchResultList.vue'
import Card from './../../components/layout/Card.vue'
import { provide, toRefs, computed } from 'vue'

export default {
    name: 'CorpusDetail',
    components: {
        Card,
        CorpusMetaCard,
        PageHeader,
        SearchResultList,
        MultiColumn
    },
    props: {
        corpusId: {
            type: Number,
            required: true
        }
    },
    setup (props) {
        const { corpusId } = toRefs(props)
        const corporaIds = computed(() => [corpusId])
        provide('corporaIds', corporaIds)
        provide('shouldStayOnSearch', true)
    }
}
</script>