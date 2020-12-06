import { Api } from './../api/Api.js'

const UserStore = {
    actions: {
        login (payload) {
            return Api.post('/login/', payload).then(response => {
                sessionStorage.setItem('auth_token', 'Token ' + response.token)
                Api.setCredentials('Token ' + response.token)
            })
        }
    }
}

export { UserStore }