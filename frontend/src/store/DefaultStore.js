import { Api } from './../api/Api.js'
import { normalizeResponse } from './helpers/NormalizeResponse.js'

function initDefaultStoreMethods (state) {
    const actions = {
        async fetchResource (path, params = {}) {
            const response = await Api.fetch(path, params)
            state.items[response.id] = response
            return response
        },
    
        async fetchResourceList (path, params = {}) {
            const response = await Api.fetch(path, params)
            state.items = normalizeResponse(response)
            return response
        },
    
        async updateResource (path, payload, params = {}) {
            let resource = state.items[payload.id]
            const newResource = { ...resource, ...payload }
            state.items[newResource.id] = newResource
            const response = await Api.patch(path, payload, params)
            return response
        }
    }
    
    return {
        actions
    }
}

export { initDefaultStoreMethods }
