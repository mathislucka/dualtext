import { onMounted, watch, computed } from 'vue'
import Project from './../store/Project.js'

const useSingleProject = (projectId) => {
    
    const fetchProject = () => {
        if (!Project.items.value[projectId.value] && Project.isLoading.value === false) {
            Project.actions.fetchProject(`/project/${projectId.value}`)
        }
    }

    const project = computed(() => Project.items.value[projectId.value] || {})

    onMounted(fetchProject)
    watch(projectId, fetchProject)

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

export { useSingleProject, useMultipleProjects, useProjectStatistics }