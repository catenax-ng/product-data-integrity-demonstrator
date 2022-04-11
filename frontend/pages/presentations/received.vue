<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Presentations Received</h1>

        <v-data-table
        :headers="headers"
        :items="presentations"
        item-key="pres_ex_id"
        sort-by="updated_at"
        sort-desc
        single-select
        >
        <template v-slot:[`item.pres_ex_id`]="{ item }">
            <div>
                <NuxtLink :to="/presentation/ + item.pres_ex_id">
                    {{ item.pres_ex_id | filterLength(6) }}...
                </NuxtLink>
            </div>
        </template>
        </v-data-table>
    </div>
</template>

<script>
export default {
    filters: {
        filterLength (value, length) {
            return value.slice(0, length) || value
        }
    },
    data: () => {
        return {
            presentations: [],
            headers: [
                { text: 'ID', value: 'pres_ex_id' },
                { text: 'state', value: 'state' },
                { text: 'Role', value: 'role' },
                { text: 'Updated At', value: 'updated_at' },
                { text: 'Connection ID', value: 'connection_id' },
            ],
        }
    },
    async fetch () {
        const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/presentation-requests', { params: { state: 'done' } })
        this.presentations = data
    }

}
</script>
