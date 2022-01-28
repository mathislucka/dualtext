<template>
        <page-header />
        <multi-column>
            <task-card />
            <project-progress-card class="md:col-span-2 md:row-span-2" />
            <task-card task-type="review" />
        </multi-column>
</template>

<script>
import ProjectProgressCard from './ProjectProgressCard.vue'
import TaskCard from './TaskCard.vue'
import PageHeader from './../../components/shared/PageHeader.vue'
import MultiColumn from './../../components/layout/MultiColumn.vue'
import { useSingleProject } from './../../composables/useProjects.js'
import { provide, toRefs, computed } from 'vue'

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
        provide('projectId', projectId)
        const { project } = useSingleProject(projectId)
        provide('project', project)
        const corporaIds = computed(() => project.value.corpora || [])
        provide('corporaIds', corporaIds)

    }
}
</script>