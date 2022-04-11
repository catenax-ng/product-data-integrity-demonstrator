<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <v-expansion-panels style="flex: 0 0 60px; margin-top: 20px;">
      <v-expansion-panel>
        <v-expansion-panel-header>Debugging Details</v-expansion-panel-header>
        <v-expansion-panel-content>
          <pre>{{ data }}</pre>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
export default {
  props: {
    data: Object
  }
}
</script>
