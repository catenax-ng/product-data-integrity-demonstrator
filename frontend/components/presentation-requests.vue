<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
      <v-data-table
        :headers="headers"
        :search="search"
        :items="records"
        item-key="pres_ex_id"
        sort-by="created_at"
        sort-desc
        single-select
        :show-select="showSelect"
        @item-selected="itemSelected"
      >
        <template v-slot:[`item.pres_ex_id`]="{ item }">
            <div>
                <NuxtLink :to="'/presentation/request/received/' + item.pres_ex_id">
                    {{ item.pres_ex_id }}
                </NuxtLink>
            </div>
        </template>
      </v-data-table>

    </div>
</template>

<script>
export default {
    filters: {
        filterTypes (value) {
            const filtered = value.filter(item => item !== 'VerifiableCredential')
            const out = filtered.join(' ')
            return out
        },
        filterLength (value, length) {
            return value.slice(0, length) || value
        }
    },
    props: {
        showSelect: Boolean,
        valueObject: Boolean, // if true, return the whole object instead of only the record id
        requestState: String,
    },
    data: () => {
        return {
            headers: [
                { text: 'Record ID', value: 'pres_ex_id' },
                { text: 'Created at', value: 'created_at' },
                { text: 'Connection ID', value: 'connection_id' },
            ],
            records: [],
            search: '',

        }
    },
    async fetch () {
        console.log('presentation-request fetch()')
        const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/presentation-requests', { params: { state: this.requestState } })
        console.log(data)
        this.records = data
    },
    watch: {
    },
    methods: {
        itemSelected (selected) {
            console.log('selected: ', selected)
            if (selected.value) {
                if (this.valueObject) {
                    this.$emit('selected', selected.item)
                } else {
                    this.$emit('selected', selected.item.record_id)
                }
            } else if (this.valueObject) {
                    this.$emit('selected', {})
                } else {
                    this.$emit('selected', '')
                }
        },
    }

}
</script>
