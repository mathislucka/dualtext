import { computed, reactive } from 'vue'
import { Api } from './../api/Api.js'

const state = reactive({
    user: {}
})

const UserStore = {
    actions: {
        login (payload) {
            return Api.post('/login/', payload).then(response => {
                sessionStorage.setItem('auth_token', 'Token ' + response.token)
                Api.setCredentials('Token ' + response.token)
                this.fetchCurrentUser()
            })
        },
        fetchCurrentUser () {
            Api.fetch('/user/current').then(response => {
                state.user = response
                console.log(state.user)
            })
        }
    },
    user: computed(() => state.user)
}

export { UserStore }