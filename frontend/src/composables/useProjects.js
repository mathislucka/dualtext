import { onMounted, watch, computed } from 'vue'
import Project from './../store/Project.js'

const useSingleProject = (projectId) => {
    
    const fetchProject = () => {
        console.log('attempting to fetch project', projectId)
        if (!Project.items.value[projectId.value]) {
            console.log('fetching project')
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

export { useSingleProject }