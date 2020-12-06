import { ref, onMounted, watch } from 'vue'
import Project from './../store/Project.js'

const useSingleProject = (id) => {
    let project = ref({})
    
    const fetchProject = async () => {
        project.value = await Project.actions.fetchProject(`/project/${id}`)
            .then(() => Project.getters.getProject(id))
    }

    onMounted(fetchProject)
    watch(id, fetchProject)

    return {
        project,
        fetchProject
    }
}

export { useSingleProject }