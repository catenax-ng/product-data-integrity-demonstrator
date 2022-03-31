<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <h1>Details</h1>
    <v-text-field v-model="node_id" label="Node ID / Link" />
    <v-btn :to="`/details/${node_id_encoded}`">
      Open
    </v-btn>
  </div>
</template>

<script>
import { encode } from 'base64url'

export default {
  data () {
    return {
      node_id: ''
    }
  },
  computed: {
    node_id_encoded () {
      return encode(this.node_id)
    }
  }
}
</script>
