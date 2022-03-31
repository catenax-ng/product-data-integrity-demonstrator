<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <v-text-field v-model="node_id" label="Node ID / Link" />
    <br>
    <graph-view :head="node_id" />
  </div>
</template>

<script>

export default {
  data () {
    return {
      node_id: '',
      data: {}
    }
  }
}
</script>
