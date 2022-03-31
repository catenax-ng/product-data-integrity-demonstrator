/* eslint-disable vue/v-slot-style */
<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Request Attestation</h1>
        <h3>Select a Connection</h3>
        <v-select
            :items="connections"
            item-text="alias"
            item-value="connection_id"
            label="Connection"
            v-model="connectionSelected"
        />
        <h3>Select a Type</h3>
        <v-select
            :items="['ContentConfirmationCredential', 'Co2ConfirmationCredential']"
            label="Type"
            v-model="typeSelected"
        />
        <div v-if="typeSelected == 'ContentConfirmationCredential'">
            <h3>Provide Request Details</h3>
            <v-text-field v-model="dataObject.nodeId" label="Node ID" />
            <v-text-field v-model="dataObject.dataId" label="Data ID" />
            <v-text-field v-model="dataObject.dataType" label="Data Type" />
            <v-text-field v-model="dataObject.dataKey" label="Key" />
            <v-text-field v-model="dataObject.dataValue" label="Value" />
            <v-btn :disabled="!formIsReady" @click="requestAttestation">Request</v-btn>
        </div>
        <div v-if="typeSelected == 'Co2ConfirmationCredential'">
            <h3>Provide Node ID</h3>
            <v-text-field v-model="dataObject.nodeId" label="Node ID" />
            <v-btn :disabled="!formIsReadyCo2" @click="requestAttestationCo2">Request</v-btn>
        </div>
    </div>
</template>

<script>
import { decode } from 'base64url'

export default {
    data: () => {
        return {
            connections: [],
            connectionSelected: '',
            dataObject: {},
            credentials: [],
            headers: [
                { text: 'Record ID', value: 'record_id' },
                { text: 'Type', value: 'cred_value.type' },
                { text: 'Issuance Date', value: 'cred_value.issuanceDate' },
                { text: 'Issuer', value: 'cred_value.issuer' },
            ],
            search: '',
            selected: [],
            typeSelected: 'ContentConfirmationCredential',
        }
    },
    async fetch () {
        const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/connections')
        this.connections = data
    },
    computed: {
        formIsReady () {
            if (!this.connectionSelected) { return false }
            if (!this.dataObject.nodeId) { return false }
            if (!this.dataObject.dataId) { return false }
            if (!this.dataObject.dataType) { return false }
            if (!this.dataObject.dataKey) { return false }
            if (!this.dataObject.dataValue) { return false }

            return true
        },
        formIsReadyCo2 () {
            if (!this.connectionSelected) { return false }
            if (!this.dataObject.nodeId) { return false }

            return true
        },
},
    mounted () {
        try {
            const prefill = this.$route.query.prefill
            this.typeSelected = this.$route.query.type
            console.log(prefill)
            const prefill_decoded = JSON.parse(decode(prefill))
            console.log(prefill_decoded)
            this.dataObject = prefill_decoded
        } catch {}
    },
    methods: {
        async requestAttestation () {
            const data = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/request-data-attestation', { data_proof: this.dataObject, connection_id: this.connectionSelected })
            console.log(data)
            this.$router.push('/attestations/received')
        },
        async requestAttestationCo2 () {
            const input = {
                proof: {
                    nodeId: this.dataObject.nodeId,
                    co2Sum: ''
                },
                connection_id: this.connectionSelected
            }
            const data = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/request-co2-attestation', input)
            console.log(data)
            this.$router.push('/attestations/received')
        }
    },

}
</script>
