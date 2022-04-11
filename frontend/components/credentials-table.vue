<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <v-row v-if="showReload">
            <v-spacer />
            <v-btn @click="$fetch"><v-icon>mdi-refresh</v-icon></v-btn>
        </v-row>
      <v-data-table
        :headers="headers"
        :search="search"
        :items="credentials"
        item-key="record_id"
        sort-by="cred_value.issuanceDate"
        sort-desc
        single-select
        :show-select="showSelect"
        @item-selected="itemSelected"
      >
        <template v-slot:[`item.record_id`]="{ item }">
            <div>
                <NuxtLink :to="/attestations/ + item.record_id">
                    {{ item.record_id | filterLength(6) }}...
                </NuxtLink>
            </div>
        </template>
        <template v-slot:[`item.cred_value.type`]="{ item }">
            <div>
                <pre>{{ item.cred_value.type | filterTypes }}</pre>
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
        disableFetch: Boolean, // do not fetch data, but use given props data
        credentialsData: Array,
        showReload: Boolean,
    },
    data: () => {
        return {
            headers: [
                { text: 'Record ID', value: 'record_id' },
                { text: 'Type', value: 'cred_value.type' },
                { text: 'Issuance Date', value: 'cred_value.issuanceDate' },
                { text: 'Issuer', value: 'cred_value.issuer' },
            ],
            credentials: [],
            search: '',

        }
    },
    async fetch () {
        console.log(this.$props.credentialsData)
        if (this.$props.disableFetch) {
            console.log('Not fetch data, since it is given via attributes / properties')
            return
        }
        console.log('credentials-table fetch()')
        const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/credentials')
        console.log(data)
        this.credentials = data
    },
    watch: {
        credentialsData (value) {
            console.log(value)
            this.credentials = value
        }
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
