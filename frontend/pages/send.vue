<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Send</h1>
        <connections-table show-search @selected="connectionId = $event" />
        <credentials-table show-select @selected="credential = $event" />
        <v-btn :disabled="!formIsReady" @click="sendCredential">Send</v-btn>
        <p v-if="!formIsReady">Please select a connection and a credential / attestation</p>
    </div>
</template>

<script>
export default {
    data: () => {
        return {
            connectionId: '',
            credential: '',
        }
    },
    computed: {
        formIsReady () {
            if (!this.connectionId) { return false }
            if (!this.credential) { return false }
            return true
        },
    },
    methods: {
        sendCredential () {
            console.log('sending credential ', this.connectionId, ' ', this.credential)
        },
    }

}
</script>
