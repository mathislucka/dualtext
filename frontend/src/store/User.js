import { computed, reactive } from 'vue'
import { Api } from './../api/Api.js'

const state = reactive({
    user: {},
    statistics: {}
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
            if (Object.keys(state.user).length === 0) {
                Api.fetch('/user/current').then(response => {
                    state.user = response
                })
            }
        },
        fetchUserStatistics () {
            Api.fetch('/user/current/statistics').then(response => {
                state.statistics = response
            })
        }
    },
    user: computed(() => state.user),
    statistics: computed(() => state.statistics)
}

export { UserStore }