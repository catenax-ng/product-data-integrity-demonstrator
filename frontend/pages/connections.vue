<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <h2>Add new connection by public DID</h2>
          <v-text-field v-model="invitePublicDid" label="Public DID"></v-text-field>
          <v-text-field v-model="alias" label="Connection Name"></v-text-field>
        <v-btn @click="addNewConnection">Add</v-btn>
        <br>
      <br>
      <h2>Connections</h2>
      <v-data-table
        v-model="selected"
        :headers="headers"
        :search="search"
        :items="connections"
        item-key="connection_id"
        show-select
        sort-by="cred_value.issuanceDate"
        sort-desc
      />

  </div>
</template>

<script>
export default {
    data: () => {
        return {
            invitePublicDid: '',
            alias: '',
            headers: [
                { text: 'Connection Name', value: 'alias' },
                { text: 'Their DID', value: 'their_did' },
                { text: 'Their Public DID', value: 'their_public_did' },
                { text: 'Our DID', value: 'my_did' },
                { text: 'Connection ID', value: 'connection_id' },
            ],
            search: '',
            connections: [],
            selected: [],
        }
    },
    async fetch () {
        const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/connections')
        this.connections = data
    },
    methods: {
        async addNewConnection () {
            const data = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/connect', { did: this.invitePublicDid, alias: this.alias })
            console.log(data)
            this.invitePublicDid = ''
            this.alias = ''
            this.$router.app.refresh()
        }
    }

}
</script>
