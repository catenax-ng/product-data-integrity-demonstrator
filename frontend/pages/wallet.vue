<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Wallet Information</h1>
        <v-text-field v-model="walletInfo.did" label="DID" readonly />
        <v-text-field v-model="walletInfo.verkey" label="Verkey" readonly />
        <v-text-field v-model="walletInfo.wallet_token" label="Wallet Token" readonly />
        <v-checkbox v-model="walletInfo.did_register_nym" label="Nym registered on the Ledger"></v-checkbox>
        <v-checkbox v-model="walletInfo.did_published" label="DID published on the Ledger"></v-checkbox>
        <debugging-info :data="walletInfo" />
    </div>
</template>

<script>
export default {
    data: () => {
        return {
            walletInfo: {},
        }
    },
    async fetch () {
        const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/info')
        this.walletInfo = data
    },

}
</script>
