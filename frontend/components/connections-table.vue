<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <v-text-field
            v-model="search"
            label="Search Connection"
            class="mx-4"
        />
        <v-data-table
            :headers="headers"
            :search="search"
            :items="connections"
            item-key="connection_id"
            show-select
            single-select
            @item-selected="selected"
        />
    </div>
</template>

<script>
export default {
    props: {
        showSearch: Boolean,
    },
    data: () => {
        return {
            headers: [
                { text: 'Connection Name', value: 'alias' },
                { text: 'Their DID', value: 'their_did' },
                { text: 'Their Public DID', value: 'their_public_did' },
                { text: 'Our DID', value: 'my_did' },
                { text: 'Connection ID', value: 'connection_id' },
            ],
            connections: [],
            search: '',
        }
    },

    async fetch () {
        console.log('connection-table asyncData')
        const data = await fetch(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/connections').then(res => res.json())
        console.log(data)
        this.connections = data
    },
    methods: {
        selected (selected) {
            console.log('selected: ', selected)
            if (selected.value) {
                this.$emit('selected', selected.item.connection_id)
            } else {
                this.$emit('selected', '') // unselect
            }
        }
    }

}
</script>
