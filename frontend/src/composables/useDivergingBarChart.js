import { axisLeft, create, range, scaleBand, scaleLinear } from 'd3'
import { ref, watch } from 'vue'
function computeIdx (idx) {
    if (idx === 0) {
        return idx
    }
    if (idx === 1) {
        return idx - 1
    }
    return idx % 2 === 1 ? idx - 2 : idx - 1
}
function createDivergingBarChart(data) {
    const margin = { top: 0, right: 60, bottom: 10, left: 60 }
    const barHeight = 33
    const width = 480
    const height = Math.ceil((data.length / 2 + 0.1) * barHeight) + margin.top + margin.bottom

    const y = scaleBand()
        .domain(range(data.length))
        .rangeRound([margin.top, height * 2 - margin.bottom])
        .padding(0.1)

    const dataValues = data.map(d => d.value)
    const x = scaleLinear()
        .domain([ Math.min(...dataValues), Math.max(...dataValues)])
        .rangeRound([ margin.left, width - margin.right ])
    
    const yAxis = g => g
        .attr("transform", `translate(${x(0)},0)`)
        .attr('class', 'text-blue-700')
        .call(axisLeft(y).tickValues([]))
    
    const svg = create('svg')
        .attr('viewBox', [0, 0, width, height])
        .attr('width', width)
  
    svg.append('g')
        .selectAll('rect')
        .data(data)
        .join('rect')
        .attr('fill', d => d.color)
        .attr('x', d => x(Math.min(d.value, 0)))
        .attr('y', (d, i) => console.log('i is', i) || y(computeIdx(i)))
        .attr('width', d => Math.abs(x(d.value) - x(0)))
        .attr('height', y.bandwidth())
    
    svg.append('g')
        .attr('fill', 'black')
        .attr('text-anchor', 'end')
        .attr('font-size', 14)
        .selectAll('text')
        .data(data)
        .join('text')
        .attr('x', d => x(d.value))
        .attr('y', (d, i) => y(computeIdx(i)) + (y.bandwidth() / 2))
        .attr('dy', '0.35em')
        .attr('dx', -8)
        .text(d => Math.abs(d.value))
        .call(text => text.filter(d => x(d.value) - x(0) < 20)
            .attr('dx', +8)
            .attr('fill', 'black')
            .attr('text-anchor', 'start'))
    
    svg.append('g')
        .call(yAxis)

    return svg.node()
}

function useDivergingBarChart (data) {
    const html = ref('')
    watch(data, () => {
        const inter = document.createElement('div')
        const svg = createDivergingBarChart(data.value)
        inter.appendChild(svg)
        html.value = inter.innerHTML
    })

    return {
        html
    }
}

export { useDivergingBarChart }