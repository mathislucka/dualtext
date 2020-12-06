import { computed, reactive } from 'vue'
import { v4 as uuidv4 } from 'uuid'

let state = reactive([])

const actions = {
    addNotification (notification) {
        notification.id = uuidv4()
        state.push(notification)
    },

    removeNotification (id) {
        const idx = state.findIndex(notification => notification.id === id)
        if (idx > -1) {
            state.splice(idx, 1)
        }
    }
}

const getters = {
    getNotifications: computed(() => state)
}

const NotificationStore = {
    actions,
    getters
}

export { NotificationStore }