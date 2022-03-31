<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <v-app>
    <v-app-bar app :color="theme.primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn to="/" text>
        Type Tree - {{ organization_name }}
      </v-btn>
      <v-spacer />
      <p>BOM as planned - Sachnummern</p>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app>
      <v-list v-if="$store.state.settings.tenant !=='' ">
        <v-list-item link to="/manage">
          <v-icon>mdi-database-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Manage Type Information</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/nodes">
          <v-icon>mdi-graph</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Tree</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/wallet">
          <v-icon>mdi-card-account-details-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Wallet</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/connections">
          <v-icon>mdi-network-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Connections</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/attestations">
          <v-icon>mdi-checkbox-marked-circle-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Request Attestations</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/attestations/received/">
          <v-icon>mdi-email-seal-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Attestations Received</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/presentation/requests/">
          <v-icon>mdi-checkbox-marked-circle-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Request Proof</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/presentations/received">
          <v-icon>mdi-email-seal-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Proofs Received</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/inbox">
          <v-icon>mdi-inbox-arrow-down-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Requests Received</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/settings">
          <v-icon>mdi-cog-outline</v-icon>
          <p>&nbsp;</p>
          <v-list-item-title>Settings</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="ma-5">
      <nuxt />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data: () => {
    return {
      theme: {
          primary: '#FFFFFF'
      },
      organization_name: '',
      drawer: null
    }
  },
  async fetch () {
      console.log(this.$config.API_PREFIX)
      // TODO: we should cache this in localStorage
      const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/config')
      console.log(data)
      this.theme = data.theme
      this.organization_name = data.organization_name
  },
  fetchOnServer: false
}
</script>
