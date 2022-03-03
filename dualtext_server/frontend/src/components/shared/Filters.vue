<template>
    <div class="flex">
        <div class="flex items-center mr-4">
            <span class="mr-2 text-xs">Methods:</span>
            <multiselect
                :selection="selectedMethods"
                :items="methods"
                @selection-changed="updateFilters"
                class="w-64"
                :borders="false" />
        </div>
    </div>
</template>

<script>
import { inject, computed, watch, onMounted, ref } from 'vue'
import { useCorpora } from '../../composables/useCorpora'
import Multiselect from './Multiselect.vue'
import { useSingleProject } from '../../composables/useProjects'
import Search from './../../store/Search.js'
import { onBeforeRouteLeave, useRoute } from 'vue-router'

export default {
  name: 'Filters',
  components: {
      Multiselect
  },
  methods: {
      updateFilters (selection) {
          this.currentFilters = { method: Object.values(selection) }
      }
  },
  setup (props, context) {
    const route = useRoute()
    const projectId = inject('projectId', null)
    let currentProject = ref({})
    if (projectId) {
        const { project } = useSingleProject(projectId)
        currentProject = project
    }

    onMounted(Search.actions.fetchSearchMethods)

    watch(currentProject, () => {
        currentFilters.value = { corpus: currentProject.value.corpora }
    })

    watch(Search.availableMethods, () => {
        if (currentFilters.value.method && currentFilters.value.method.length === 0) {
            currentFilters.value = { method: [Search.availableMethods.value[0]] }
        }
    })

    const currentFilters = computed({
        get: () => Search.selectedFilters.value,
        set: (val) => {
            Search.actions.setSelectedFilters({ ...Search.selectedFilters.value, ...val })
        }
    })

    onMounted(() => {
        if (!route.query || Object.keys(route.query).length === 0) {
            currentFilters.value = {
                ...Search.availableMethods[0] ? { method: [ Search.availableMethods.value[0] ]} : {method: []},
                ...projectId ? { corpus: currentProject.value.corpora } : {},
                ...projectId ? { project: projectId.value } : {},
            }
        }
    })


    const transformedMethods = computed(() => {
        return Search.availableMethods.value.reduce((acc, curr, idx) => {
            acc[idx] = curr
            return acc
        }, {})
    })

    const selectedMethods = computed(() => {
        let transformed
        if (currentFilters.value.method && currentFilters.value.method.length) {
            transformed = currentFilters.value.method.reduce((acc, curr) => {
                const originalMethodId = Object.entries(transformedMethods.value).find(([key, value]) => value === curr)
                if (originalMethodId) {
                    acc[originalMethodId[0]] = curr
                }
                return acc
            }, {})
        } else {
            transformed = [ Object.values(transformedMethods.value)[0] ]
        }
        return transformed
    })

    return {
        currentFilters,
        methods: transformedMethods,
        selectedMethods
    }
  }
}
</script>