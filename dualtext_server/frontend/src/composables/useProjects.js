import { onMounted, watch, computed } from 'vue'
import Project from './../store/Project.js'

const fetchProject = (projectId) => {
    if (!Project.items.value[projectId] && Project.isLoading.value === false) {
        return Project.actions.fetchProject(`/project/${projectId}`)
    }
}

const useSingleProject = (projectId) => {

    const project = computed(() => Project.items.value[projectId.value] || {})

    onMounted(() => {
        fetchProject(projectId.value)
    })
    watch(projectId, () => {
        if (projectId.value !== -1) {
            fetchProject(projectId.value)
        }
    })

    return {
        project,
        fetchProject
    }
}

const useMultipleProjects = () => {
    const fetchProjects = () => {
        const isCached = Project.requests.value.find(request => request.type === 'list')
        if (!Project.isLoading.value && !isCached) {
            Project.actions.fetchProjectList('/project/')
        }
    }

    onMounted(fetchProjects)

    return {
        projects: Project.items
    }
}

function useProjectStatistics (projectId) {
    onMounted(() => {
        if (projectId.value) {
            Project.actions.fetchProjectStatistics(projectId.value)
        }
    })

    watch(projectId, () => {
        if (projectId.value) {
            Project.actions.fetchProjectStatistics(projectId.value)
        }
    })

    return {
        projectStatistics: Project.statistics
    }
}

export { useSingleProject, useMultipleProjects, useProjectStatistics, fetchProject }