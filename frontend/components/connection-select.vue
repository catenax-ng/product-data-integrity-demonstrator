<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <v-select
        v-model="selected"
        :items="connections"
        item-text="alias"
        item-value="connection_id"
        label="Connection"
    >
        <template v-slot:[`item`]="{ item }">
            <p>{{ item.alias }}</p>&nbsp;<p v-if="showId">ID:{{ item.connection_id }}</p>&nbsp;<p v-if="showDid">DID:{{ item.their_did }}</p>
        </template>
    </v-select>

</template>

<script>
export default {
    props: {
        showId: Boolean,
        showDid: Boolean,
    },
    data: () => {
        return {
            connections: [],
            selected: '',
        }
    },

    async fetch () {
        console.log('connection-select asyncData')
        const data = await fetch(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/connections').then(res => res.json())
        console.log(data)
        this.connections = data
    },
    watch: {
        selected (value) {
            console.log('selected: ', value)
            this.$emit('selected', value)
        }
    }

}
</script>
