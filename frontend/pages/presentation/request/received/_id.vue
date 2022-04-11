<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Request Received</h1>
        <v-text-field v-model="record.pres_ex_id" label="Request ID" readonly />
        <v-text-field v-model="record.state" label="State" readonly />

        <v-text-field :value="field" label="Field" readonly />
        <v-text-field :value="pattern" label="Pattern" readonly />
        <h3>Credentials in Wallet that match the request</h3>
        <credentials-table :credentials-data="credentials" disable-fetch show-select @selected="credential = $event" />
        <v-btn @click="reply()" :disabled="!formIsReady">Reply with Credential</v-btn>
        <p v-if="!formIsReady">Please select a Credential to reply with. Only requests in state request-received can be answered.</p>
    </div>
</template>

<script>
export default {
    data: () => {
        return {
            record: {},
            credentials: [],
            pattern: '',
            field: '',
            credential: '',
        }
    },
    async fetch () {
        // don't use incjections { params } and 'this' will be available and data can be accessed (and axios...)!
        const params = this.$route.params
        console.log('requests/received: parmas', params)
        const { data: record } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/presentation-request/' + params['id'])
        console.log(record)
        this.record = record

        const { data: credentials } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/presentation-request/' + params['id'] + '/credentials')
        this.credentials = credentials
    },
    computed: {
        formIsReady () {
            if (this.record.state !== 'request-received') { return false }
            if (this.credential === '') { return false }

            return true
        }
    },
    watch: {
        record (value) {
            const pattern = value.by_format?.pres_request?.dif?.presentation_definition?.input_descriptors[0]?.constraints?.fields[0]?.filter?.pattern
            const field = value.by_format?.pres_request?.dif?.presentation_definition?.input_descriptors[0]?.constraints?.fields[0]?.path[0]
            console.log(pattern)
            this.pattern = pattern
            this.field = field
        }
    },
    methods: {
        async reply () {
            const { data } = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/presentation-request/' + this.record.pres_ex_id + '/send/' + this.credential)
            console.log(data)
        }
    }

}
</script>
