import { Api } from './../api/Api.js'
import { normalizeResponse } from './helpers/NormalizeResponse.js'

function handleCache (state, requestType) {
    const id = new Date().getTime() + Math.random()
    state.requests.push({ type: requestType, id })

    setTimeout(() => {
        state.requests = state.requests.filter(request => request.id !== id)
    }, 120000)
}

function initDefaultStoreMethods (state) {
    const actions = {
        async fetchResource (path, params = {}) {
            state.isLoading = true
            const response = await Api.fetch(path, params)
            state.items[response.id] = response
            state.isLoading = false
            handleCache(state, 'fetch')
            return response
        },
    
        async fetchResourceList (path, params = {}, strategy) {
            state.isLoading = true
            const response = await Api.fetch(path, params)
            const { items, order } = normalizeResponse(response)
            if (strategy === 'append') {
                state.items = { ...state.items, ...items }
            } else {
                state.items = items
            }
            state.order = order
            state.isLoading = false
            handleCache(state, 'list')
            return response
        },
    
        async updateResource (path, payload, params = {}) {
            let resource = state.items[payload.id]
            const newResource = { ...resource, ...payload }
            // optimisically update state
            state.items[newResource.id] = newResource
            let response = null
            try {
                response = await Api.patch(path, payload, params)
            } catch {
                // reset state on error
                state.items[resource.id] = resource
            }
            handleCache(state, 'update')
            return response
        },

        resetStore () {
            state.isLoading = false
            state.items = {}
            state.order = []
            state.requests = []
        }
    }
    
    return {
        actions
    }
}

export { initDefaultStoreMethods }
