<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Send Presentation Request</h1>
        <h3>Select a Coonection</h3>
        <connections-table @selected="connectionId = $event" />
        <h3>Select a Node ID</h3>
        <v-text-field v-model="co2RequestNodeId" label="Node ID" />
        <v-btn @click="sendCo2Request()" :disabled="!formIsReady">Send new CO2 Request</v-btn>
        <p v-if="!formIsReady">Please provide a Node ID and select the connection from where you wan to request the Proof</p>
        <br><hr><br>
        <h1>Requests Sent</h1>
        <presentation-requests request-state="request-sent" />
    </div>
</template>

<script>
export default {
    data: () => {
        return {
            co2RequestNodeId: '',
            connectionId: '',
        }
    },
    fetch () {
        console.log('TODO: load list from server')
    },
    computed: {
        formIsReady () {
            if (this.connection_id === '') { return false }
            if (this.co2RequestNodeId === '') { return false }
            return true
        }
    },
    methods: {
        async sendCo2Request () {
            console.log(this.co2RequestNodeId, this.connectionId)
            const data = {
                node_id: this.co2RequestNodeId,
                connection_id: this.connectionId

            }
            await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/presentation/request/co2sum', data)

            this.$fetch()
        }
    }
}
</script>
