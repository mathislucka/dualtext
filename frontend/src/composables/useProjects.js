import { ref, onMounted, watch, computed } from 'vue'
import Project from './../store/Project.js'

const useSingleProject = (projectId) => {
    
    const fetchProject = () => {
        Project.actions.fetchProject(`/project/${projectId.value}`)
    }

    const project = computed(() => Project.items.value[projectId] || {})

    onMounted(fetchProject)
    watch(projectId, fetchProject)

    return {
        project,
        fetchProject
    }
}

export { useSingleProject }