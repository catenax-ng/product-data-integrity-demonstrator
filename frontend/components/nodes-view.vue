<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <v-text-field v-model="start_url" label="Node ID / Link / URL Starting Point" />
    <v-checkbox v-model="show_previous" label="Show 'previous' / history (in grey dashed links)" />
    <v-btn @click="start"><v-icon>mdi-send</v-icon>Start</v-btn>
    <v-btn @click="next_level"><v-icon>mdi-next</v-icon>Next</v-btn>

    <div>
      <v-text-field v-model="type_data.type_name" label="Type Name" readonly />
      <v-text-field v-model="type_data.version" label="Version" readonly />
      <v-text-field v-model="selected_node_id" label="Node ID / Link" readonly />
      <v-checkbox label="Is a 'remote' type (managed by a supplier)" readonly :value="isRemoteType(selected_node_id)" />
    </div>

    <div id="mynetwork" />

    <div v-if="type_data.type_name">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>Details</v-expansion-panel-header>
          <v-expansion-panel-content>
            <pre>{{ type_data }}</pre>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>

  </div>
</template>

<script>
import { Network } from 'vis-network'

export default {

  data: function () {
    return {
      nodes: new Set(),
      edges: [
      ],
      network: null,
      start_url: '',
      current_level_node_ids: [],
      show_previous: false,
      selected_node_id: '',
      type_data: {}
    }
  },
  mounted: function () {
    this.redraw()
  },
  methods: {
    start () {
      console.log('start')
      // TODO: use backend API because of authentication with remote systems
      // for now, do it right in the browser
      this.nodes = new Set()
      this.edges = []
      this.current_level_node_ids = new Set([this.start_url])
      this.nodes.add(this.start_url)
      this.redraw()
    },
    async next_level () {
      let next_level = new Set()
      for (const item of this.current_level_node_ids) {
        const current_node_id = item
        const { data } = await this.$axios.get(current_node_id)
        const new_nodes = data.nodes
        const new_edges = data.nodes.map((n) => { return { from: current_node_id, to: n, arrows: 'to' } })
        if (this.show_previous) {
          if (data.previous && data.previous.length > 0) {
            // new_nodes.push({ id: data.previous, label: '...' + data.previous.slice(-6), color: 'red' })
            new_nodes.push(data.previous)
            new_edges.push({ from: current_node_id, to: data.previous, color: 'grey', dashes: true, arrows: 'to' })

            next_level.add(data.previous)
          }
        }
        this.nodes = new Set([...this.nodes, ...new_nodes]) // a Set contains only unique elements
        this.edges = this.edges.concat(new_edges)
        console.log(data.nodes)
        next_level = new Set([...next_level, ...data.nodes])
      }

      this.current_level_node_ids = next_level
      console.log(this.current_level_node_ids)
      this.redraw()
    },
    isRemoteType (node_url) {
      /**
       * "remoteType" in this context / view means: the hostname part of the url is
       * different to the one from the start_url
       */
      let start_url_hostname = ''
      try {
        start_url_hostname = new URL(this.start_url).host
      } catch { return false }

      let url_hostname = ''
      try {
        url_hostname = new URL(node_url).host
      } catch { return false }

      const remote = (url_hostname !== start_url_hostname)
      return remote
    },
    redraw () {
      const el = document.getElementById('mynetwork')

      const nodes = this.nodes.map((n) => {
        let color = '#2B7CE9'
        if (this.isRemoteType(n)) {
          color = 'black'
        }
        return { id: n, label: '...' + n.slice(-6), color: { border: color, highlight: { border: color } } }
      }) // create the actual vis structure here to avaoid double entries in arrays
      const data = { nodes: Array.from(nodes), edges: this.edges }
      this.network = new Network(el, data, { height: '500px', width: '100%', layout: { hierarchical: { enabled: true, direction: 'UD', sortMethod: 'directed' } } })
      this.network.on('selectNode', this.nodeSelected)
      this.network.on('deselectNode', this.nodeDeselected)
    },
    async nodeSelected (params) {
      console.log(params)
      const node_id = params.nodes[0]
      console.log(node_id)
      this.selected_node_id = node_id
      const { data } = await this.$axios.get(node_id)
      for (const item of data.data) {
        if (item.type === this.$config.ITEMTYPE_TYPE) {
          const type_result = await this.$axios.get(item.url)
          this.type_data = type_result.data
          // const type_data = type_result.data
          // this.type_data = JSON.parse(type_data)
          console.log(this.type_data)
        }
      }
    },
    nodeDeselected (params) {
      this.selected_node_id = ''
      this.type_data = {}
    }
  }
}
</script>
