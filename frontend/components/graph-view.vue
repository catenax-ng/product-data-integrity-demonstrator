<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <div>
      <v-text-field v-model="type_data.type_name" label="Type Name" readonly />
      <v-text-field v-model="type_data.version" label="Version" readonly />
      <v-text-field v-model="selected_node_id" label="Node ID / Link" readonly />
      <v-checkbox label="Is a 'remote' type (managed by a supplier)" readonly />
    </div>

    <div id="mynetwork" />
    <debugging-info :data="data" />
</div>
</template>

<script>
import { encode } from 'base64url'
import { Network } from 'vis-network'

export default {
  props: {
    head: {
      type: String,
      default: ''
    },
    b64Head: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      data: {},
      selected_node_id: '',
      type_data: {}
    }
  },
  fetch: async function () {
    let param = ''
    if (this.b64Head) {
      // use the one set via props
      param = this.b64Head
    } else {
      param = this.b64 // the computed value from the head prop
    }
    console.log('param: ', param)
    if (typeof param === 'undefined') { return }
    const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/graph/' + param)
    this.data = data
  },
  computed: {
    b64: function () {
      if (!this.head) {
        return
      }
      return encode(this.head)
    }
  },
  watch: {
    data: function () {
      this.redraw()
    },
    head: '$fetch', // watch the property and run the fetch hook again
    b64Head: '$fetch'
  },
  methods: {
    redraw () {
      console.log('redraw')
      const el = document.getElementById('mynetwork')
      if (typeof this.data.nodes === 'undefined') { return }

      const nodes = this.data?.nodes.map((n) => {
        const color = '#2B7CE9'
        /**
        if (this.isRemoteType(n)) {
          color = 'black'
        }
         */
        return { id: n, label: '...' + n.slice(-6), color: { border: color, highlight: { border: color } } }
      }) // create the actual vis structure here to avaoid double entries in arrays
      const edges = this.data.edges.map((n) => { return { from: n.from, to: n.to, arrows: 'to' } })

      const data = { nodes: Array.from(nodes), edges: edges }
      this.network = new Network(el, data, { height: '500px', width: '100%', layout: { hierarchical: { enabled: true, direction: 'UD', sortMethod: 'directed' } } })
      this.network.on('selectNode', this.nodeSelected)
      this.network.on('deselectNode', this.nodeDeselected)
    },
    nodeSelected (params) {
      console.log(params)
      const node_id = params.nodes[0]
      console.log(node_id)
      this.selected_node_id = node_id
      this.type_data = this.data.type_data[node_id]
    },
    nodeDeselected (params) {
      this.selected_node_id = ''
      this.type_data = {}
    }

  }
}
</script>
