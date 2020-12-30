import { axisLeft, create, range, scaleBand, scaleLinear, max } from 'd3'
import { watch, ref } from 'vue'

function createBarChart (data) {
    console.log(data)
    const margin = { top: 10, right: 0, bottom: 10, left: 0 }
    const barHeight = 33
    const height = Math.ceil((data.length + 0.1) * barHeight) + margin.top + margin.bottom
    const width = 600 // make responsive later
    const y = scaleBand()
        .domain(range(data.length))
        .rangeRound([margin.top, height - margin.bottom])
        .padding(0.1)

    const x = scaleLinear()
        .domain([0, max(data, d => d.value)])
        .range([margin.left, width - margin.right])
    
    const yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
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
        .attr('x', x(0))
        .attr('y', (d, i) => y(i))
        .attr('width', d => x(d.value) - x(0))
        .attr('height', y.bandwidth())

    svg.append('g')
        .attr('fill', 'black')
        .attr('text-anchor', 'end')
        .attr('font-size', 14)
        .selectAll('text')
        .data(data)
        .join('text')
        .attr('x', d => x(d.value))
        .attr('y', (d, i) => y(i) + (y.bandwidth() / 2))
        .attr('dy', '0.35em')
        .attr('dx', -8)
        .text(d => d.value)
        .call(text => text.filter(d => x(d.value) - x(0) < 20)
            .attr('dx', +8)
            .attr('fill', 'black')
            .attr('text-anchor', 'start'))
    
    svg.append('g')
        .call(yAxis)

    return svg.node()
}

function useBarChart (data) {
    let html = ref('')
    watch(data, () => {
        const svg = createBarChart(data.value)
        const intermediate = document.createElement('div')
        intermediate.appendChild(svg)
        console.log(intermediate)
        html.value = intermediate.innerHTML
    })

    return {
        html
    }
}

export { useBarChart }
