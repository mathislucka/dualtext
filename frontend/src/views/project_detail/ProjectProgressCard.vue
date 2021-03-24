<template>
    <card class="overflow-auto">
        <template v-slot:header>
            <h2 class="font-semibold text-xl text-grey-800">Project Statistics</h2>
        </template>
        <template v-slot:content>
            <div class="w-full">
                <h3 class="font-semibold text-lg text-grey-600 mb-2">Annotation Progress</h3>
                <div class="flex flex-wrap">
                    <swatch v-for="swatch in divergingBarChartData" :key="swatch.key" :swatch="swatch" />
                </div>
                <div v-html="divergingHtml" />

                <h3 class="font-semibold text-lg text-grey-600 mt-8">Label distribution</h3>
                <div id="chart" v-html="barHtml"></div>
                <div class="flex flex-wrap">
                    <swatch v-for="swatch in swatches" :key="swatch.key" :swatch="swatch" />
                </div>

                <h3 class="font-semibold text-lg text-grey-600 mt-8">Progress over Time</h3>
                <div><svg id="timeseries" /></div>
            </div>
        </template>
    </card>
</template>

<script>
import { useBarChart } from './../../composables/useBarChart.js'
import { useProjectLabels } from './../../composables/useLabels.js'
import { useProjectStatistics } from './../../composables/useProjects.js'
import { useDivergingBarChart } from './../../composables/useDivergingBarChart.js'
import { useTimeseriesChart } from './../../composables/useTimeseriesChart.js'
import Card from '../../components/layout/Card.vue'
import Swatch from './Swatch.vue'
import { computed, inject } from 'vue'

export default {
    name: 'ProjectProgressCard',
    components: {
        Card,
        Swatch
    },
    setup () {
        const projectId = inject('projectId')
        const { labels } = useProjectLabels(projectId)
        const { projectStatistics } = useProjectStatistics(projectId)
        const preparedData = computed(() => {
            let retVal = []
            const labelStats = projectStatistics.value.labels
            if (labelStats) {
                retVal = Object.entries(labelStats.absolute)
                    .map(([key, value]) => {
                        const label = labels.value.find(label => label.name === key)
                        return {
                            key,
                            value: parseInt(value),
                            color: label ? label.color.standard : 'steelblue'
                        }
                    })
                    .sort((a, b) => b.value - a.value)
            }
            return retVal
        })
        const { html } = useBarChart(preparedData, '#chart')

        const divergingBarChartData = computed(() => {
            let retVal = []
            if (projectStatistics.value.annotations) {
                const { annotations } = projectStatistics.value
                retVal = [
                    {
                        key: 'Open Annotations',
                        value: parseInt(annotations.open_annotations) * -1,
                        color: '#FC839C'
                    },
                    {
                        key: 'Closed Annotations',
                        value: parseInt(annotations.annotated_absolute),
                        color: '#97E8D8'
                    },
                    {
                        key: 'Open Reviews',
                        value: parseInt(annotations.open_reviews) * -1,
                        color: '#FFF880'
                    },
                    {
                        key: 'Closed Reviews',
                        value: parseInt(annotations.reviewed_absolute),
                        color: '#81BEFE'
                    },
                ]
            }
            return retVal
        })

        const timeseriesData = computed(() => {
            if (projectStatistics.value.timetracking && projectStatistics.value.timetracking.timeseries) {
                const previousSum = (idx, data) => {
                    const previous = data.slice(0, idx + 1)
                    return previous.map(val => val.count).reduce((acc, val) => acc + val)
                }
                return projectStatistics.value.timetracking.timeseries.map((day, idx) => {
                    const remaining = projectStatistics.value.annotations.total - previousSum(idx, projectStatistics.value.timetracking.timeseries)
                    return {
                        ...day,
                        date: new Date(day.date),
                        remaining: remaining < 0 ? 0 : remaining
                    }
                })
            }
            return []
        })

        const result = useDivergingBarChart(divergingBarChartData)
        const timeseries = useTimeseriesChart(timeseriesData)

        return {
            swatches: preparedData,
            barHtml: html,
            divergingHtml: result.html,
            divergingBarChartData,
            //timeseriesHtml: timeseries.html
            timeseriesData
        }
    }
}
</script>