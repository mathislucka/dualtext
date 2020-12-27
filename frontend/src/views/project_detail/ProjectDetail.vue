<template>
        <page-header />
        <multi-column>
            <task-card />
            <task-card task-type="review" />
        </multi-column>
</template>

<script>
import TaskCard from './TaskCard.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import { provide, toRefs } from 'vue'

export default {
    name: 'ProjectDetail',
    components: {
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