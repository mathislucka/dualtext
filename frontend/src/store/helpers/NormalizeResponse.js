function normalizeResponse (apiResponse) {
    let items = {}
    let order = []
    if (Array.isArray(apiResponse)) {
        apiResponse.forEach(resource => {
            items[resource.id] = resource
            order.push(resource.id)
        })
    } else {
        items[apiResponse.id] = apiResponse
    }

    return { items, order }
}

export { normalizeResponse }