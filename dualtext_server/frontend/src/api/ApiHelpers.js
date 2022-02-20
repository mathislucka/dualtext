function serializeParams(params) {
    let serializedParams = ''
    const paramList = Object.entries(params).reduce((acc, [key, value]) => {
        if (Array.isArray(value)) {
            acc = [ ...acc, ...serializeArray(value, key)]
        } else {
            acc.push(key + '=' + encodeURIComponent(value))
        }
        return acc
    }, [])
    serializedParams = paramList.length > 0 ? '?' + paramList.join('&') : serializedParams
    return serializedParams
}

function serializeArray(arr, key) {
    return arr.reduce((acc, val) => {
        acc.push(key + '=' + encodeURIComponent(val))
        return acc
    }, [])
}

async function safe (promise) {
    let returnVal = {}
    try {
        const response = await promise
        if (!response.ok) {
            returnVal = { error: response.json(), response: null }
        } else {
            returnVal = { error: null, response: response.json() }
        }
        return returnVal
    } catch(e) {
        returnVal = { error: e, response: null }
    }
   return returnVal
}

export { safe, serializeParams }