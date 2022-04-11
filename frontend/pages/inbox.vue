<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Proof Requests Received</h1>
        <presentation-requests request-state="request-received" />
        <h1>Attestation Requests Received</h1>
    </div>
</template>

<script>
import presentationRequests from '../components/presentation-requests.vue'
export default {
  components: { presentationRequests },

}
</script>
