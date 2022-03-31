import colors from 'vuetify/es5/util/colors'

export default {
  // Target: https://go.nuxtjs.dev/config-target
  // target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - TypeTree-UI',
    title: 'TypeTree-UI',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    'jsondiffpatch/dist/formatters-styles/html.css'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
      '~/plugins/settings.client.js',
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios'
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: '/'
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: [],
    theme: {
      dark: false,
      themes: {
        light: {
          primary: process.env.THEME_PRIMARY_COLOR || colors.blue,
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107'
        },
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },

  publicRuntimeConfig: {
    ITEMTYPE_TYPE: process.env.ITEMTYPE_TYPE || 'http://supplytree.org/ns/ItemType',
    tenant: '',
    API_PREFIX: process.env.API_PREFIX || ''
  },

  server: {
    host: process.env.HOST || '0.0.0.0',
    port: process.env.PORT || 3000
  },
  ssr: false, // we don't want server rendering! this could have saved us a lot of debugging ;-)
  alias: {
    '@interop/did-web-resolver': '/node_modules/@interop/did-web-resolver/dist/index.js',
    '@digitalcredentials/did-io': '/node_modules/@digitalcredentials/did-io/dist/index.js',
    '@digitalcredentials/lru-memoize': '/node_modules/@digitalcredentials/lru-memoize/dist/index.js'
  },
  buildDir: process.env.BUILD_DIR || '.nuxt',
  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    buildDir: process.env.BUILD_DIR || '.nuxt'
  }
}
