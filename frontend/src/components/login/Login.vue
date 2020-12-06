<template>
    <div class="m-auto absolute top-0 bottom-0 left-0 right-0 w-1/3 border border-grey-300 rounded shadow flex flex-col p-4 h-64">
        <div class="mb-4 w-full">
            <label for="username" class="block mb-2 font-semibold">Username</label>
            <input
                type="text"
                id="username"
                class="w-full border rounded border-grey-300 shadow px-4 py-2 focus:ring-2"
                v-model="username"
                @keyup.enter="loginUser">
        </div>
        <div class="mb-4">
            <label for="password" class="block mb-2 font-semibold">Password</label>
            <input
                type="password"
                id="password"
                class="w-full border rounded border-grey-300 shadow px-4 py-2 focus:ring-2"
                v-model="password"
                @keyup.enter="loginUser">
        </div>
        <div class="flex content-right">
            <button
                type="button"
                class="px-4 py-2 text-white bg-blue-500 rounded shadow ml-auto mr-0 hover:bg-blue-600"
                @click="loginUser">
                    Submit
            </button>
        </div>
    </div>
</template>

<script>
import { UserStore } from './../../store/User.js'
export default {
    name: 'Login',
    data () {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        loginUser () {
            UserStore.actions.login({ username: this.username, password: this.password })
        }
    }
}
</script>