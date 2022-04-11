<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <h1>Identity</h1>
    <pre>{{ didDocument }}</pre>
  </div>
</template>

<script>
import { Ed25519VerificationKey2020 }
  from '@digitalbazaar/ed25519-verification-key-2020'
import { X25519KeyAgreementKey2020 }
  from '@digitalbazaar/x25519-key-agreement-key-2020'
import { CryptoLD } from 'crypto-ld'

import * as didWeb from '@interop/did-web-resolver'

const cryptoLd = new CryptoLD()
cryptoLd.use(Ed25519VerificationKey2020)
cryptoLd.use(X25519KeyAgreementKey2020)

const didWebDriver = didWeb.driver({ cryptoLd })

const DEFAULT_KEY_MAP = {
  // capabilityInvocation: 'Ed25519VerificationKey2020',
  authentication: 'Ed25519VerificationKey2020',
  assertionMethod: 'Ed25519VerificationKey2020'
  // capabilityDelegation: 'Ed25519VerificationKey2020',
  // keyAgreement: 'X25519KeyAgreementKey2020'
}

export default {
  data () {
    return {
      didDocument: ''
    }
  },
  mounted () {
    this.didDocument = 'Loading...'
    this.initIdentity()
  },
  methods: {
    async initIdentity () {
      const url = 'https://oem.demo.supplytree.org'
      const { didDocument, keyPairs } = await didWebDriver.generate({ url, keyMap: DEFAULT_KEY_MAP })
      this.didDocument = didDocument
      console.log(didDocument)
      console.log(keyPairs)
    }
  }
}
</script>
