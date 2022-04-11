<!--
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
-->
<template>
    <div>
        <h1>Presentation</h1>
        <v-text-field v-model="record.pres_ex_id" label="Request ID" readonly />
        <v-text-field v-model="record.state" label="State" readonly />
        <v-text-field v-model="record.verified" label="Verified" readonly >
            <template v-slot:append>
                <v-icon v-if="record.verified === 'True'" color="green">mdi-shield-check</v-icon>
            </template>
        </v-text-field>
        <v-text-field v-model="record.created_at" label="Created at" readonly />
        <v-text-field v-model="record.updated_at" label="Updated at" readonly />
        <v-text-field v-model="record.role" label="Role" readonly />
        <div v-if="record.state === 'done'">
            <v-textarea
                v-model="vc"
                label="Verifiable Presentation"
                style="font-size: small;"
                rows="20"
            />
            <v-btn @click="verify()">Verify</v-btn>
            <br><br>
            <v-row>
                <p class="pt-5" >Presentation Verified</p>
                <v-icon style="font-size: 40px" v-if="vp_verified.presentation_verified" color="green">mdi-shield-check</v-icon>
                <v-icon style="font-size: 30px" v-else color="red">mdi-close-circle</v-icon>
            </v-row>
            <v-row>
                <p class="pt-5">All Verifiable Credentials Verified</p>
                <v-icon style="font-size: 40px" v-if="vp_verified.all_vcs_verified" color="green">mdi-shield-check</v-icon>
                <v-icon style="font-size: 30px" v-else color="red">mdi-close-circle</v-icon>
            </v-row>
        </div>

        <debugging-info :data="record" />
    </div>
</template>

<script>
export default {
    data: () => {
        return {
            record: {},
            vc: '',
            vp_verified: {},
        }
    },
    async fetch () {
        // don't use incjections { params } and 'this' will be available and data can be accessed (and axios...)!
        const params = this.$route.params
        console.log('presentation/_id: parmas', params)
        const { data: record } = await this.$axios.get(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/presentation-request/' + params['id'])
        console.log(record)
        this.record = record
        if (record.state === 'done') {
            const pres = record?.pres['presentations~attach'][0]?.data?.json
            delete pres['presentation_submission']
            this.vc = JSON.stringify(pres, null, 4)
        }
    },
    computed: {
    },
    watch: {
    },
    methods: {
        async verify () {
            const vc = JSON.parse(this.vc)
            console.log(vc)
            const { data: vp_verified } = await this.$axios.post(this.$config.API_PREFIX + '/' + this.$store.state.settings.tenant + '/wallet/verify', vc)
            console.log(vp_verified)
            this.vp_verified = vp_verified
        }
    }

}
</script>
