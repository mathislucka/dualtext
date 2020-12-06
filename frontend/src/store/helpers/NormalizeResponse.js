function normalizeResponse (apiResponse) {
    let normalizedResponse = {}
    if (Array.isArray(apiResponse)) {
        apiResponse.forEach(resource => {
            normalizedResponse[resource.id] = resource
        })
    } else {
        normalizedResponse[apiResponse.id] = apiResponse
    }

    return normalizedResponse
}

export { normalizeResponse }