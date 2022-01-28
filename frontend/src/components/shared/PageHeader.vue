<template>
    <header>
        <div class="flex">
            <main-menu class="w-20" />
            <search class="w-full" />
            <div class="text-5xl text-teal-500 flex items-center border-b border-teal-500 w-64 hidden md:block">
                <span class="ml-4">dualtext</span>
            </div>
            <div class="md:hidden flex items-center content-center mr-4">
                <button
                    @click="toggleFilters"
                    class="btn-icon">
                    <icon icon="filter" height="16" width="16" />
                </button>
            </div>
        </div>
        <div
            class="flex"
            :class="{ 'hidden': showFilters, 'md:flex': showFilters }">
            <filters class="w-full md:ml-20 md:mr-64 ml-4 mr-4" />
        </div>
    </header>
</template>

<script>
import Filters from './Filters.vue'
import MainMenu from './MainMenu.vue'
import Icon from './Icon.vue'
import Search from './Search.vue'
import SearchStore from './../../store/Search.js'
import { useCorpora } from './../../composables/useCorpora.js'
import { toRefs } from 'vue'
export default {
    name: 'PageHeader',
    components: {
        Icon,
        Filters,
        MainMenu,
        Search,
    },
    data () {
        return {
            showFilters: true
        }
    },
    methods: {
        toggleFilters () {
            this.showFilters = !this.showFilters
        }
    }
}
</script>