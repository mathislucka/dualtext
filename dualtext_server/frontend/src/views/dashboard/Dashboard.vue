<template>
        <page-header />
        <multi-column>
            <project-card class="overflow-auto" />
            <user-statistics-card class="row-span-2 col-span-2" />
            <corpora-card class="overflow-auto" />
        </multi-column>
</template>

<script>
import PageHeader from './../../components/shared/PageHeader.vue'
import CorporaCard from './CorporaCard.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import ProjectCard from './ProjectCard.vue'
import UserStatisticsCard from './UserStatisticsCard.vue'

export default {
    name: 'Dashboard',
    components: {
        PageHeader,
        CorporaCard,
        MultiColumn,
        ProjectCard,
        UserStatisticsCard
    }
}
</script>