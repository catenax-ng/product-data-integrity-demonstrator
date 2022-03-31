<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <h1>Attestation Details</h1>
    <v-text-field v-model="attestation.cred_value.issuer" label="Issuer" readonly />
    <v-text-field v-model="attestation.cred_value.issuanceDate" label="Issuance Date" readonly />
    <v-text-field v-model="attestation.cred_value.type" label="Type" readonly />
    <div>
    <small>Credential Subject</small>
    <pre>{{ attestation.cred_value.credentialSubject }}</pre>
    </div>

    <debugging-info :data="attestation" />
  </div>
</template>

<script>
import debuggingInfo from '../../components/debugging-info.vue'

export default {
  components: { debuggingInfo },
  async asyncData ({ params, $config, store }) {
    console.log('_id page: ', params)
    const details = params['id']
    if (!details) {
      return
    }
    console.log('details to be fetched: ', details)
    const data = await fetch($config.API_PREFIX + '/' + store.state.settings.tenant + '/wallet/credential/' + details).then(res => res.json())
    console.log(data)

    return {
        attestation: data
    }
  },
  data () {
      return {
          // attestation: { cred_value: {} }
      }
  },
  fetchOnServer: false,
  methods: {

  },
  filters: {
      toString (value) {
          const out = JSON.stringify(value)
          return out
      }
  }
}
</script>
