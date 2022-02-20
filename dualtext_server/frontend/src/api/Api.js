import { serializeParams } from './ApiHelpers.js'
import { NotificationStore } from './../store/Notify.js'

const ApiBuilder = class {
    constructor (baseUrl) {
        this.baseUrl = baseUrl
        this.headers = {
            'Content-Type': 'application/json'
        }
        const token = sessionStorage.getItem('auth_token')
        if (token) {
            this.setCredentials(token)
        }
    }

    async genericFetch (method, path, payload, params) {
        const url = this.baseUrl + path + serializeParams(params)
        let returnVal = {}
        try {
            const response = await fetch(url, {
                method: method,
                mode: 'cors',
                credentials: 'include',
                headers: this.headers,
                ...payload ? { body: JSON.stringify(payload) } : {}
            })
            console.log(response)
            if (!response.ok) {
                returnVal = { error: await response.json(), response: null }
            } else {
                returnVal = { error: null, response: await response.json() }
            }
        } catch(e) {
            returnVal = { error: 'An error occurred. Try to reload the page.', response: null }
        }

        if (returnVal.error) {   
            NotificationStore.actions.addNotification({ type: 'error', content: await returnVal.error })
            throw new Error('Something went wrong')
        }

        return returnVal.response
    }
    
    async fetch (path, params = {}) {
        const response = await this.genericFetch('GET', path, null, params)
        return response
    }

    async post (path, payload, params = {}) {
        const response = await this.genericFetch('POST', path, payload, params)
        return response
    }

    async patch (path, payload, params = {}) {
        const response = await this.genericFetch('PATCH', path, payload, params)
        return response 
    }

    async delete (path, params = {}) {
        const response = await this.genericFetch('DELETE', path, null, params)
        return response 
    }

    setCredentials (token) {
        this.headers = { ...this.headers, 'Authorization': token }
    }

    removeCredentials () {
        delete this.headers.Authorization
    }
}

const Api = new ApiBuilder(import.meta.env.VITE_API_URL)

export { Api }