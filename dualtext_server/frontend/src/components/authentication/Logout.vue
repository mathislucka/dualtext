<template>
    <div></div>
</template>

<script>
import { UserStore } from './../../store/User.js'

export default {
    name: 'Logout',
    created() {
        UserStore.actions.logout().then(() => {
            this.$router.push({ name: 'login' })
        })
    }
}
</script>