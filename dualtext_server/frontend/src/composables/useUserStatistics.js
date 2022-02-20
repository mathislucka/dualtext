import { onMounted } from 'vue'
import { UserStore } from './../store/User.js'

function useUserStatistics () {
    onMounted(UserStore.actions.fetchUserStatistics)

    return {
        statistics: UserStore.statistics
    }
}

export { useUserStatistics }