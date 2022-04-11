<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <v-simple-table>
      <thead>
        <tr>
          <th>Type Name</th>
          <th>Version</th>
          <th>Node ID / Link</th>
          <th>Edit</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, key) in type_data" :key="key">
          <td v-if="editable == key && !edit_object.node.id">
            <v-text-field v-model="edit_object.type_details.type_name" label="Type Name" />
            <br>OR
            <v-text-field v-model="new_type_node_url" label="Node ID / Link" />
          </td>
          <td v-else>
            {{ item.type_details.type_name }}
          </td>

          <td v-if="editable == key" style="vertical-align:top">
            <v-text-field v-model="edit_object.type_details.version" label="Version" />
          </td>
          <td v-else>
            {{ item.type_details.version }}
          </td>
          <td>
            <a v-if="item.node.id" :href="item.node.id">Node Link</a>
          </td>

          <td v-if="editable == key" style="vertical-align:top;padding:10px">
            <v-btn @click="update">
              Save
            </v-btn>
            <v-btn @click="cancel_update">
              Cancel
            </v-btn>
          </td>
          <td v-else>
            <v-btn @click="edit(key)">
              <v-icon>mdi-square-edit-outline</v-icon>
            </v-btn>
            <NuxtLink :to="/details/ + encodeData(item.node.id)">
              Details
            </NuxtLink>
            &nbsp;
            <NuxtLink :to="/graph/ + encodeData(item.node.id)">
              Graph
            </NuxtLink>
          </td>
        </tr>
      </tbody>
    </v-simple-table>

    <v-fab-transition>
      <v-btn
        color="pink"
        dark
        absolute
        bottom
        right
        fab
        style="margin-bottom: 50px"
        @click="add"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>

    <br>
    <div v-if="editable">
      <h2>Child Types</h2>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search child types"
        single-line
        hide-details
      />
      <v-data-table
        v-model="selected"
        :headers="headers"
        :search="search"
        :items="type_list"
        item-key="node.id"
        show-select
      />
    </div>
  </div>
</template>

<script>
import { encode } from 'base64url'

export default {
  data: () => ({
    editable: '',
    edit_object: {},
    type_data: {},
    headers: [
      { text: 'Type Name', value: 'type_details.type_name' }
    ],
    new_type_node_url: '',
    search: '',
    selected: []
  }),

  async fetch () {
    const { data } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/types')
    this.type_data = data.data
  },
  fetchOnServer: false,

  computed: {
    type_list: function () {
      return Object.values(this.type_data) || []
    }
  },

  methods: {
    edit (id) {
      this.editable = id
      this.edit_object = this.type_data[id]
      this.selected = this.type_data[id].type_details.child_types.map((x) => { return { node: { id: x } } })
    },
    async update () {
      // adding by Node ID / Link?
      if (this.new_type_node_url.length > 0) {
        const node_add_result = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/ItemType/by-link', { url: this.new_type_node_url })
        console.log(node_add_result)
        if (node_add_result.status === 200) {
          const result_data = node_add_result.data
          this.type_data[result_data.type_details.type_name] = result_data
          delete this.type_data.dummy
          this.$router.app.refresh()
        }
        // consider errors
        console.log(node_add_result.detail)
        return
      }
      // manually adding / updating type information
      console.log(this.edit_object)
      console.log(this.selected)
      const child_types = this.selected.map(x => x.node.id)
      this.edit_object.type_details.child_types = child_types
      const input = { type_details: this.edit_object.type_details }
      input.previous = this.edit_object.node.id
      const { data } = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/ItemType', input)
      console.log(data)
      // update local copy and avoid reloading the list from the server
      this.type_data[data.type_details.type_name] = data
      this.editable = ''
      // if 'dummy' in the list from adding, just remove
      delete this.type_data.dummy
    },
    cancel_update () {
      this.editable = ''
      delete this.type_data.dummy
    },
    add () {
      const dummy = {
        node: {
        },
        type_details: {
          version: '',
          type_name: ''
        }
      }
      this.type_data['dummy'] = dummy
      this.edit_object = dummy
      this.editable = 'dummy'
    },
    encodeData (data) {
      return encode(data)
    }
  }

}
</script>

<style>
</style>
