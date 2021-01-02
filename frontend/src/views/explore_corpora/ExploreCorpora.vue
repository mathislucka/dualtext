<template>
        <page-header />
        <multi-column :columns="1">
            <card :use-header="false">
                <template v-slot:content>
                    <search-result-list />
                </template>
            </card>
        </multi-column>
</template>

<script>
import SearchResultList from './../../components/shared/SearchResultList.vue'
import Card from './../../components/layout/Card.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import { provide, toRefs } from 'vue'

export default {
    name: 'ProjectDetail',
    components: {
        SearchResultList,
        Card,
        PageHeader,
        MultiColumn
    }
}
</script>