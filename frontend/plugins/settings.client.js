/*
 Copyright (c) 2022 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/catenax-ng/product-data-integrity-demonstrator

 SPDX-License-Identifier: Apache-2.0
*/

export default ({ store, inject }) => {
    console.log('settings.client.js')
    if (process.server) { return }

    const tenant = localStorage.getItem('tenant')
    console.log('tenant: ', tenant)
    if (tenant) {
        store.commit('settings/setTenant', tenant)
    }
}
