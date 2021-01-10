<template>
    <div class="flex">
        <div class="flex items-center w-1/2 mr-4">
            <span class="mr-2 text-xs">Methods:</span>
            <multiselect
                :selection="methods"
                :items="methods"
                @selection-changed="updateFilters($event, 'methods')"
                class="w-full"
                :borders="false" />
        </div>
        <div class="flex items-center w-1/2">
            <span class="mr-2 text-xs">Corpora:</span>
            <multiselect
                :selection="corpora"
                :items="corpora"
                @selection-changed="updateFilters($event, 'corpora')"
                class="w-full"
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

export default {
  name: 'Filters',
  components: {
      Multiselect
  },
  methods: {
      updateFilters (selection, type) {
          if (type === 'corpora') {
              this.currentFilters = { corpus: Object.keys(selection) }
          }
          if (type === 'methods') {
              this.currentFilters = { method: Object.values(selection) }
          }
      }
  },
  setup (props, context) {
      const projectId = inject('projectId', null)
      const corpusId = inject('corpusId', null)
      let currentProject = ref({})
      if (projectId) {
        const { project } = useSingleProject(projectId)
        currentProject.value = project
      }

      const { corpora } = useCorpora(currentProject)

      const transformedCorpora = computed(() => {
        const transformed = corpora.value.reduce((acc, corpus) => {
            acc[corpus.id] = corpus.name
            return acc
        }, {})
        return corpusId ? { [corpusId.value]: transformed[corpusId.value] } : transformed
      })

      watch(corpora, () => {
          currentFilters.value = { corpus: corpora.value.map(c => c.id ) }
      })

      const currentFilters = computed({
          get: () => Search.selectedFilters.value,
          set: (val) => {
              Search.actions.setSelectedFilters({ ...Search.selectedFilters.value, ...val })
          }
      })

      return {
          currentFilters,
          corpora: transformedCorpora,
          methods: { '1': 'elastic', '2': 'sentence_embedding' }
      }
  }
}
</script>