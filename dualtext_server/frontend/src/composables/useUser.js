import { UserStore } from './../store/User.js'

function useUser () {
    UserStore.actions.fetchCurrentUser()
    return {
        user: UserStore.user
    }
}

export { useUser }