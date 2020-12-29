<template>
        <page-header />
        <multi-column>
            <task-card />
            <project-progress-card class="col-span-2 row-span-2" />
            <task-card task-type="review" />
        </multi-column>
</template>

<script>
import ProjectProgressCard from './ProjectProgressCard.vue'
import TaskCard from './TaskCard.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import { provide, toRefs } from 'vue'

export default {
    name: 'ProjectDetail',
    components: {
        ProjectProgressCard,
        TaskCard,
        PageHeader,
        MultiColumn
    },
    props: {
        projectId: {
            type: Number,
            required: true
        }
    },
    setup (props) {
        const { projectId } = toRefs(props)
        const projectProvider = provide('projectId', projectId)

        return {
            projectProvider
        }
    }
}
</script>