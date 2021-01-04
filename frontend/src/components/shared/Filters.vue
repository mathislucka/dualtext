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
import { useCorpora, useMultipleCorpora } from '../../composables/useCorpora'
import Multiselect from './Multiselect.vue'
import { useSingleProject } from '../../composables/useProjects'
export default {
  name: 'Search',
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
      let corpora
      if (projectId) {
        const { project } = useSingleProject(projectId)
        const corporaWrapper = useCorpora(project)
        corpora = corporaWrapper.corpora
      } else {
        const corporaWrapper = useMultipleCorpora()
        corpora = corporaWrapper.corpora
      }

      const transformedCorpora = computed(() => {
        return corpora.value.reduce((acc, corpus) => {
            acc[corpus.id] = corpus.name
            return acc
        }, {})
      })

      const filters = ref({
          method: { '1': 'elastic', '2': 'sentence_embedding' },
          corpus: null
      })

      const currentFilters = computed({
          get: () => ({
              method: Object.values(filters.value.method),
              corpus: Object.keys(filters.value.corpus || transformedCorpora.value ),
              ...projectId ? { project: projectId.value } : {}
            }),
          set: (val) => {
              filters.value = { ...filters.value, ...val }
          }
      })
      watch(currentFilters, () => {
          context.emit('filters-changed', currentFilters)
      })

      return {
          currentFilters,
          corpora: transformedCorpora,
          methods: { '1': 'elastic', '2': 'sentence_embedding' }
      }
  }
}
</script>