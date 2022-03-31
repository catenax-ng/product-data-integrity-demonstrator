<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <h1>Settings</h1>
    <v-color-picker
        v-model="picker"
        class="ma-2"
        show-swatches
    />
    <v-text-field v-model="config.organization_name" label="Organization Name" />
    <v-btn @click="updateSettings()">Send</v-btn>
  </div>
</template>

<script>
export default {
    async asyncData ({ $config, store }) {
        const data = await fetch($config.API_PREFIX + '/' + store.state.settings.tenant + '/config').then(res => res.json())
        console.log(data)
        return {
            config: data
        }
    },
    data: () => {
        return {
            picker: {},
            config: { theme: {} },
        }
    },
    methods: {
        async updateSettings () {
            const input = this.config
            input.theme.primary = this.picker.hexa
            console.log(input)
            const { data } = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/config', input)
            console.log(data)
            window.location.reload()
        }
    }
}
</script>
