<template>
    <div class="flex flex-col md:flex-row">
        <div class="flex items-center md:w-1/2 w-full mr-4">
            <span class="mr-2 text-xs">Methods:</span>
            <multiselect
                :selection="selectedMethods"
                :items="methods"
                @selection-changed="updateFilters($event, 'methods')"
                class="w-full"
                :borders="false" />
        </div>
        <div class="flex items-center w-1/2">
            <span class="mr-2 text-xs">Corpora:</span>
            <multiselect
                :selection="selectedCorpora"
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
import { onBeforeRouteLeave, useRoute } from 'vue-router'

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
    const route = useRoute()
    const projectId = inject('projectId', null)
    const corporaIds = inject('corporaIds', ref(null))
    let currentProject = ref({})
    if (projectId) {
        const { project } = useSingleProject(projectId)
        currentProject.value = project
    }
    const { corpora } = useCorpora(currentProject)
    onMounted(Search.actions.fetchSearchMethods)
    
    const transformedCorpora = computed(() => {
        let transformed = corpora.value.reduce((acc, corpus) => {
            acc[corpus.id] = corpus.name
            return acc
        }, {})

        if (corporaIds.value) {
            transformed = corporaIds.value.reduce((acc, corpusId) => {
                const corpus = transformed[corpusId]
                if (corpus) {
                    acc[corpusId] = corpus
                }
                return acc
            }, {})
        }
        return transformed
    })
    const selectedCorpora = computed(() => {
        let transformed
        if (currentFilters.value.corpus && currentFilters.value.corpus.length) {
            transformed = currentFilters.value.corpus.reduce((acc, curr) => {
                const corpus = corpora.value.find(corpus => corpus.id === parseInt(curr))
                if (corpus) {
                    acc[curr] = corpus.name
                }
                return acc
            }, {})
        } else {
            transformed = transformedCorpora.value
        }
        if (corporaIds.value) {
            transformed = corporaIds.value.reduce((acc, corpusId) => {
                const corpus = transformed[corpusId]
                if (corpus) {
                    acc[corpusId] = corpus
                }
                return acc
            }, {})
        }
        return transformed
    })

    watch(corpora, () => {
        setCorpusFilter()
    })

    watch(corporaIds, () => {
        setCorpusFilter()
    })

    const setCorpusFilter = () => {
        if (currentFilters.value.corpus && currentFilters.value.corpus.length === 0) {
            const result = { corpus: corpora.value.map(c => c.id ).filter(id => corporaIds.value === null || corporaIds.value.includes(id)) }
            currentFilters.value = result
        }
    }

    watch(Search.availableMethods, () => {
        if (currentFilters.value.method && currentFilters.value.method.length === 0) {
            currentFilters.value = { method: Search.availableMethods.value }
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
                method: Search.availableMethods.value,
                corpus: corpora.value.map(c => c.id ).filter(id => corporaIds.value === null || corporaIds.value.includes(id)),
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
            transformed = transformedMethods.value
        }
        return transformed
    })

    return {
        currentFilters,
        corpora: transformedCorpora,
        methods: transformedMethods,
        selectedCorpora,
        selectedMethods
    }
  }
}
</script>