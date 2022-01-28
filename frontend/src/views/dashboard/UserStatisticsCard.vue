<template>
    <card>
        <template v-slot:header>
            <h2 class="font-semibold text-xl text-grey-800">Work Done</h2>
        </template>
        <template v-slot:content>
            <div id="chart" class="md:flex w-full justify-center"></div>
        </template>
    </card>
</template>

<script>
import { useUserStatistics } from './../../composables/useUserStatistics.js'
import { useDonut } from './../../composables/useDonutChart.js'
import { computed } from 'vue'

import Card from '../../components/layout/Card.vue'
export default {
    name: 'UserStatisticsCard',
    components: {
        Card
    },
    setup () {
        const { statistics } = useUserStatistics()

        const transformedStatistics = computed(() => {
            const { annotations } = statistics.value

            const returnVal = annotations
                ? {
                    ...annotations.annotator.open > 0
                        ? { 'Open Annotations': annotations.annotator.open }
                        : {},
                    ...annotations.annotator.closed > 0
                        ? { 'Closed Annotations': annotations.annotator.closed }
                        : {},
                    ...annotations.reviewer.open > 0
                        ? { 'Open Reviews': annotations.reviewer.open }
                        : {},
                    ...annotations.reviewer.closed > 0
                        ? { 'Closed Reviews': annotations.reviewer.closed }
                        : {}
                }
                : {}
            return returnVal
        })

        useDonut(transformedStatistics, '#chart')
    }
}
</script>