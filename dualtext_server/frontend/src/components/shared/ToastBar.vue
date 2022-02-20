<template>
    <div
        v-if="notifications"
        class="absolute top-4 right-4 z-99 w-96 flex flex-col">
        <toast
            v-for="notification in notifications"
            :key="notification.id"
            :notification="notification"
            @close="removeNotification(notification.id)" />
    </div>
</template>

<script>
import Icon from './Icon.vue'
import { NotificationStore } from './../../store/Notify.js'
import Toast from './Toast.vue'

export default {
    name: 'ToastBar',
    components: {
        Toast
    },
    
    setup () {
        const notifications = NotificationStore.getters.getNotifications
        return {
            notifications,
            removeNotification: NotificationStore.actions.removeNotification
        }
    }
}
</script>