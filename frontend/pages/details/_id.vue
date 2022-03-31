<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <h1>Type Details</h1>
    <v-text-field v-model="type_details.type_data.type_name" label="Type Name" readonly />
    <v-text-field v-model="type_details.type_data.version" label="Version" :readonly="type_details.meta.is_remote_type" />
    <v-row>
      <v-text-field v-model="type_details.type_data.catena_x_unique_id" label="Global Identifier" readonly />
      <v-btn @click="copyGlobalIdToClipboard()"><v-icon>mdi-content-copy</v-icon></v-btn>
    </v-row>
    <v-checkbox v-model="type_details.meta.is_remote_type" label="Is a 'remote' type (managed by a supplier and can NOT be edited)" readonly />
    <br>
    <v-row v-if="childs_selected.length > 0">
      <v-spacer />
      <v-btn @click="deleteSelectedComponent()"><v-icon>mdi-delete</v-icon></v-btn>
    </v-row>
    <h3>CO2</h3>
    <v-text-field v-model="type_details.co2_data.co2" label="CO2 equivalent" />
    <h3>Built-in child components</h3>
    <v-data-table
      v-model="childs_selected"
      :headers="child_table_headers"
      :items="child_list"
      item-key="node_id"
      show-select
      hide-default-footer
    />
    <div v-if="!type_details.meta.is_remote_type">
      <h3>Available components</h3>
      <v-row>
        <v-spacer />
        <v-btn @click="buildIntoParent()"><v-icon>mdi-plus</v-icon>Build into parent</v-btn>
      </v-row>
      <v-data-table
        v-model="build_in_components_selected"
        :headers="child_table_headers"
        :items="available_types_list"
        item-key="node_id"
        show-select
        hide-default-footer
      />
    </div>
    <br>
    <v-btn v-if="!type_details.meta.is_remote_type" @click="saveChanges()">
      <v-icon>mdi-content-save</v-icon>Save changes
    </v-btn>
    <br>
    <br>
    <hr>
    <br>
    <div v-if="type_details.meta.is_remote_type">
      <v-btn @click="searchLatest()"><v-icon>mdi-refresh</v-icon>Search latest version...</v-btn>
      <br>
      <br>
      <div v-if="versions_details.newer_versions">
        <v-row>
          <v-select v-model="version_selected" label="Exact Version to compare with" :items="version_index" item-value="idx" item-text="node_id" />
          <v-btn @click="updateTypeHead()"><v-icon>mdi-send</v-icon>Update</v-btn>
        </v-row>
        <p><b>Remember:</b> Updating only changes the local database for that type, but does NOT change existing relationships between types. This needs to be done manually!</p>
        <data-diff :data1="versions_details.current_data" :data2="selected_version_data" />
        <br>

        <debugging-info :data="versions_details" />
      </div> <!-- v-if="versions_details.newer_versions" -->
    </div> <!-- v-if="type_details.meta.is_remote_type" -->
    <div v-else>
        <!-- not a remote type, but our own, that means we can request attestations for it -->

        <v-row>
            <v-col>
                <h3>Request data attestation</h3>
                <v-btn @click="requestAttestation()">
                    <v-icon>mdi-checkbox-marked-circle-outline</v-icon>
                    Request
                </v-btn>
            </v-col>
            <v-col>
                <h3>Request CO2 attestation</h3>
                <v-btn @click="requestCo2Attestation()">
                    <v-icon>mdi-checkbox-marked-circle-outline</v-icon>
                    Request CO2
                </v-btn>
            </v-col>
        </v-row>
    </div>
    <debugging-info :data="type_details" />
  </div>
</template>

<script>
import { encode } from 'base64url'
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
    const data = await fetch($config.API_PREFIX + '/' + store.state.settings.tenant + '/type/by-node-id/' + details).then(res => res.json())
    console.log(data)

    let available_types = {}
    // fetch all types if we are working on a local type that could be updated
    if (!data.meta.is_remote_type) {
      available_types = await fetch($config.API_PREFIX + '/' + store.state.settings.tenant + '/types').then(res => res.json())
      available_types = available_types.data
      console.log(available_types)
    }

    return {
      type_details: data,
      available_types: available_types
    }
  },
  data () {
    return {
      childs_selected: [],
      child_table_headers: [
        { text: 'Type Name', value: 'type_data.type_name' },
        { text: 'Type Version', value: 'type_data.version' }
      ],
      build_in_components_selected: [],
      versions_details: {},
      version_selected: 0
      // type_details: {}
    }
  },
  computed: {
    selected_version_data: function () {
      let result = {}
      try {
        result = this.versions_details.newer_versions_data[this.version_selected]
      } catch {}
      return result
    },
    version_index: function () {
      let vi = []
      try {
        vi = this.versions_details.newer_versions.map((item, idx) => { return { idx: idx, node_id: item } })
      } catch {}
      return vi
    },
    child_list: function () {
      const result = Object.entries(this.type_details.type_data.child_types).map((item, index) => {
        const node_id = item[1]
        const child_data = this.type_details?.child_types_data[node_id]?.type_data
        return { node_id: node_id, type_data: child_data }
      })
      return result
    },
    available_types_list: function () {
      const result = Object.entries(this.available_types).map((item) => {
        const node_id = item[1].node.id
        return { node_id: node_id, type_data: item[1].type_details }
      })
      return result
    }
  },
  /**
  watch: {
    versions_details () {
      console.log('versions_details changed')
      this.version_selected = 0
    }
  },
   */
  methods: {
    copyGlobalIdToClipboard () {
      navigator.clipboard.writeText(this.type_details.type_data.catena_x_unique_id)
    },
    async searchLatest () {
      const data = await fetch(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/type/new_versions/by-node-id/' + this.$route.params.id).then(res => res.json())
      this.versions_details = data
      this.version_selected = 0
    },
    updateTypeHead: async function () {
      console.log(this.version_selected)
      const node_id = this.versions_details.newer_versions[this.version_selected]
      const { data } = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/ItemType/by-link', { url: node_id })
      console.log(data)
    },
    deleteSelectedComponent () {
      console.log(this.childs_selected)

      const selected = this.childs_selected.map(n => n.node_id) // we only need an array of node_id elements
      const reduced_childs = this.type_details.type_data.child_types.filter((n) => {
        return !selected.includes(n)
      })
      console.log(reduced_childs)
      this.type_details.type_data.child_types = reduced_childs

      this.childs_selected = [] // empty to allow new selections
    },
    buildIntoParent () {
      const add = this.build_in_components_selected.map((n) => {
        //
        // TODO: dirty hack, not the best way, but should do it for now
        this.type_details.child_types_data[n.node_id] = { type_data: n.type_data }

        return n.node_id
      })
      console.log(add)
      this.type_details.type_data.child_types.push(...add)
      this.build_in_components_selected = [] // empty selection to start over
    },
    requestAttestation () {
        const prefill = {
            nodeId: this.type_details.meta.node_id,
            dataId: this.type_details.meta.data_id,
            dataType: this.type_details.meta.type,
        }
        const prefill_encoded = encode(JSON.stringify(prefill))
        this.$router.push({
            path: '/attestations',
            query: {
                prefill: prefill_encoded
            }
        })
    },
    requestCo2Attestation () {
        const prefill = {
            nodeId: this.type_details.meta.node_id,
        }
        const prefill_encoded = encode(JSON.stringify(prefill))
        this.$router.push({
            path: '/attestations',
            query: {
                prefill: prefill_encoded,
                type: 'Co2ConfirmationCredential',
            }
        })
    },
    async saveChanges () {
      console.log('saveChanges')
      const input = {
            type_details: this.type_details.type_data,
            co2_details: this.type_details.co2_data
        }

      input.previous = this.type_details.meta.node_id
      console.log(input)
      const { data } = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/ItemType', input)
      console.log(data)
      this.$router.push('/manage')
    }
  }
}
</script>
