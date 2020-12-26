import { arc, pie, select, scaleOrdinal } from 'd3'
import { onMounted, watch } from 'vue'

const COLORS = ['#97E8D8', '#FC839C', '#B2C1CC', '#FFF880', '#81BEFE']
function createDonut (data, elementSelector) {
    const width = 950
    const height = 600
    const margin = 60

    const radius = Math.min(width, height) / 2 - margin

    const svg = select(elementSelector)
        .html('')
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
        const color = scaleOrdinal()
            .domain(Object.keys(data))
            .range(COLORS)
        
        const pieFunc = pie()
            .sort(null)
            .value((d) => d.value)
        const preparedData = pieFunc(Object.entries(data).map(([k, v]) => ({ key: k, value: v })))

        const firstArc = arc()
            .innerRadius(radius * 0.5)         // This is the size of the donut hole
            .outerRadius(radius * 0.8)

        // Another arc that won't be drawn. Just for labels positioning
        const outerArc = arc()
            .innerRadius(radius * 0.9)
            .outerRadius(radius * 0.9)
        
        svg
            .selectAll('allSlices')
            .data(preparedData)
            .enter()
            .append('path')
            .attr('d', firstArc)
            .attr('fill', function(d){ return(color(d.data.key)) })
            .attr("stroke", "white")
            .style("stroke-width", "2px")
            .style("opacity", 0.7)
        
        svg
            .selectAll('allPolylines')
            .data(preparedData)
            .enter()
            .append('polyline')
              .attr("stroke", "black")
              .style("fill", "none")
              .attr("stroke-width", 1)
              .attr('points', function(d) {
                    console.log('points', d)
                    const posA = firstArc.centroid(d) // line insertion in the slice
                    const posB = outerArc.centroid(d) // line break: we use the other arc generator that has been built only for that
                    let posC = outerArc.centroid(d); // Label position = almost the same as posB
                    const midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
                    posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
                    return [posA, posB, posC]
              })
          
          // Add the polylines between chart and labels:
          svg
            .selectAll('allLabels')
            .data(preparedData)
            .enter()
            .append('text')
              .text( function(d) { return `${d.data.key} (${d.data.value})` } )
              .attr('transform', function(d) {
                  var pos = outerArc.centroid(d);
                  var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                  pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
                  return 'translate(' + pos + ')';
              })
              .style('text-anchor', function(d) {
                  var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                  return (midangle < Math.PI ? 'start' : 'end')
              })
}

function useDonut (data, elementSelector) {
    onMounted(() => {
        createDonut(data.value, elementSelector)
    })

    watch(data, () => {
        createDonut(data.value, elementSelector)
    })
}

export { useDonut }