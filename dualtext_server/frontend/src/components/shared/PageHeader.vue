<template>
    <header>
        <div class="flex">
            <main-menu class="w-20" />
            <search v-if="false" class="w-full" />
            <div class="w-full"></div>
            <div class="text-5xl text-teal-500 flex items-center border-b border-teal-500 w-64">
                <span class="ml-4">dualtext</span>
            </div>
        </div>
        <div class="flex" v-if="false">
            <filters class="w-full ml-20 mr-64" />
        </div>
    </header>
</template>

<script>
import Filters from './Filters.vue'
import MainMenu from './MainMenu.vue'
import Search from './Search.vue'
import SearchStore from './../../store/Search.js'
import { useCorpora } from './../../composables/useCorpora.js'
import { toRefs } from 'vue'
export default {
    name: 'PageHeader',
    components: {
        Filters,
        MainMenu,
        Search,
    }
}
</script>