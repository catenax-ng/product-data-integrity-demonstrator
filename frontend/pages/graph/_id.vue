<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <graph-view :b64-head="node_id" />
  </div>
</template>

<script>

export default {
  data () {
    return {
      node_id: ''
    }
  },
  created: function () {
    console.log('graph/_id')
    this.node_id = this.$route.params.id
  }

}
</script>
