<template>
    <card>
        <template v-slot:header>
            <h2 class="font-semibold text-xl text-grey-800">Your Corpora</h2>
        </template>
        <template v-slot:content>
            <ul>
                <template v-for="corpus in corpora" :key="corpus.id + 'template'">
                    <li class="mb-2">
                        <router-link
                            class="underline font-semibold text-blue-500 hover:text-blue-700"
                            :to="{ name: 'project_detail' }">
                            {{ corpus.name }}
                        </router-link>
                    </li>
                </template>
            </ul>
        </template>
    </card>
</template>

<script>
import { useMultipleCorpora } from './../../composables/useCorpora.js'

import Card from '../../components/layout/Card.vue'
export default {
    name: 'CorporaCard',
    components: {
        Card
    },
    setup () {
        const { corpora } = useMultipleCorpora()

        return {
            corpora
        }
    }
}
</script>