<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <h1>Diff</h1>

    <div id="diff" v-show="data_available"></div>
    <br>
    <v-expansion-panels v-if="showDetails">
      <v-expansion-panel>
        <v-expansion-panel-header>Details</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row>
            <pre>{{ data1 }}</pre>
            <pre>{{ data2 }}</pre>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
import { diff, formatters } from 'jsondiffpatch'

export default {

  props: {
    data1: {
      type: Object,
      default: () => {}
    },
    data2: {
      type: Object,
      default: () => {}
    },
    showDetails: Boolean
  },
  data () {
    return {
      diff: {}
    }
  },
  computed: {
    data_available () {
      if (typeof this.data1 === 'undefined') {
        return false
      }
      if (typeof this.data2 === 'undefined') {
        return false
      }
      return true
    }
  },
  watch: {
    data1: function () {
      this.redraw()
    },
    data2: function () {
      this.redraw()
    }
  },
  mounted () {
    this.redraw()
  },
  methods: {
    redraw: function () {
      const el = document.getElementById('diff')
      if (!el) {
        return // we only draw if the element is visible
      }
      const delta = diff(this.data1, this.data2)
      console.log(delta)
      el.innerHTML = formatters.html.format(delta, this.data1)
    }
  }
}
</script>
