<template>
    <card>
        <template v-slot:header>
            <h2 class="font-semibold text-xl text-grey-800">Your Projects</h2>
        </template>
        <template v-slot:content>
            <ul>
                <template v-for="project in projects" :key="project.id + 'template'">
                    <li class="mb-2">
                        <router-link
                            class="underline font-semibold text-blue-500 hover:text-blue-700"
                            :to="{ name: 'project_detail', params: { projectId: project.id } }">
                            {{ project.name }}
                        </router-link>
                    </li>
                </template>
            </ul>
        </template>
    </card>
</template>

<script>
import { useMultipleProjects } from './../../composables/useProjects.js'

import Card from '../../components/layout/Card.vue'
export default {
    name: 'ProjectCard',
    components: {
        Card
    },
    setup () {
        const { projects } = useMultipleProjects()

        return {
            projects
        }
    }
}
</script>