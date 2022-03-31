<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Type Tree Information System</h1>
        <div v-if="$store.state.settings.tenant ==='' ">
            Please create a Tenant to get started:<br>
            <v-btn @click="createTenant()">Create new tenant</v-btn>
        </div>
        <div v-else>
            <v-btn @click="logoutTenant()">Logout Tenant</v-btn>
            <br>
            You can set an organization name and a color in <NuxtLink to="/settings">Settings</NuxtLink>
        </div>
        <b>Tenant: {{ $store.state.settings.tenant }}</b>
        <br>
    </div>
</template>

<script>

export default {
    methods: {
        async createTenant () {
            const { data } = await this.$axios.post(this.$config.API_PREFIX + '/tenant')
            console.log(data)
            this.$store.commit('settings/setTenant', data.tenant)
            // window.location.reload(true)
            this.$router.app.refresh()
        },
        logoutTenant () {
            this.$store.commit('settings/setTenant', '')
            window.location.reload()
        }
    }
}
</script>
