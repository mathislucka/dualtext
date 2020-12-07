import { serializeParams } from './ApiHelpers.js'
import { NotificationStore } from './../store/Notify.js'
import { UserStore } from './../store/User.js'

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

            if (!response.ok) {
                returnVal = { error: await response.json(), response: null }
                console.log(returnVal.error.password)
            } else {
                returnVal = { error: null, response: await response.json() }
            }
        } catch(e) {
            returnVal = { error: e, response: null }
        }

        if (returnVal.error) {   
            NotificationStore.actions.addNotification({ type: 'error', content: await returnVal.error })
            throw new Error('Something went wrong')
        }

        return returnVal.response
    }
    
    async fetch (path, params = {}) {
        console.log(this.headers)
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
}

const Api = new ApiBuilder('http://localhost:8000/api/v1')

export { Api }