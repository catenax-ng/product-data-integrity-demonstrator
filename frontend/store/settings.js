/*
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
*/

export const state = () => ({
    tenant: ''
})

export const mutations = {
    setTenant (state, tenant) {
        if (process.server) { return }
        localStorage.setItem('tenant', tenant)
        state.tenant = tenant
    }
}
