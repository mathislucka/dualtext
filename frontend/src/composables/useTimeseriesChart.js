import { axisLeft, axisBottom, create, line, scaleUtc, scaleLinear, max, extent, event, select } from 'd3'
import { watch, ref } from 'vue'

function createTimeseriesChart (data) {
    console.log(data)
    if (!data || data.length === 0) {
        return
    }
    const margin = { top: 20, right: 20, bottom: 30, left: 80 }
    const barHeight = 33
    const height = 350
    const width = 600 // make responsive later
    const domain = data.map(d => d.count).concat(data.map(d => d.remaining))
    const y = scaleLinear()
        .domain([0, max(domain)]).nice()
        .range([height - margin.bottom, margin.top])
    
    const x = scaleUtc()
        .domain(extent(data, d => d.date))
        .range([margin.left, width - margin.right])

    const lines = line()
        .defined(d => !isNaN(d.count))
        .x(d => x(d.date))
        .y(d => y(d.count))
    
    const remaining = line()
        .defined(d => !isNaN(d.remaining))
        .x(d => x(d.date))
        .y(d => y(d.remaining))
    
    const circles = scaleLinear()
        .domain([0, max(data, d => d.seconds)])
        .range([5, 25])

    const xAxis = g => g
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(axisBottom(x).ticks(width / 80).tickSizeOuter(0))

    const yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(axisLeft(y))
        .call(g => g.select(".domain").remove())
        .call(g => g.select(".tick:last-of-type text").clone()
            .attr("x", 3)
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .text(data.y))

    const svg = select('#timeseries')
        .attr('viewBox', [0, 0, width, height])
        .attr('width', width)

    // svg.append('g')
    //     .selectAll('circle')
    //     .data(data)
    //     .join('circle')
    //     .attr('fill', 'steelblue')
    //     .attr('r', d => circles(d.seconds))
    //     .attr('cx', d => x(d.date))
    //     .attr('cy', d => y(d.count))
    
    // svg.append('g')
    //     .selectAll('texts')
    //     .data(data)
    //     .join('text')
    //     .attr('x', d => x(d.date) - 35)
    //     .attr('y', d => y(d.count) - circles(d.seconds) - 5)
    //     .text(d => Math.floor(d.seconds / 60))

    svg.append('g')
        .append("path")
        .datum(data)
        .attr("d", d => {
            const proj = d.filter(v => v.projected)
            const last = d[d.length - (proj.length + 1)]
            console.log(last)
            return lines([last, ...proj])
        })
        .attr("fill", "none")
        .attr("stroke", "currentColor")
        .attr('class', 'text-teal-300')
        .attr("stroke-width", 2)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")

    svg.append('g')
        .append("path")
        .datum(data)
        .attr("d", d => lines(d.filter(v => !v.projected)))
        .attr("fill", "none")
        .attr("stroke", "currentColor")
        .attr('class', 'text-teal-500')
        .attr("stroke-width", 2)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")

    svg.append('g')
        .append("path")
        .datum(data)
        .attr("d", d => remaining(d))
        .attr("fill", "none")
        .attr("stroke", "currentColor")
        .attr('class', 'text-teal-500')
        .attr("stroke-width", 2)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
    console.log(remaining)
    console.log(x)

    svg.append("g")
        .call(xAxis)

    svg.append("g")
        .call(yAxis)

    return svg
}

function useTimeseriesChart (data) {
    let html = ref('')
    watch(data, () => {
        const svg = createTimeseriesChart(data.value)
        //select('#timeseries').append(svg)
        // const intermediate = document.createElement('div')
        // intermediate.appendChild(svg)
        // html.value = intermediate.innerHTML
    })

    return {
        html
    }
}

export { useTimeseriesChart }
