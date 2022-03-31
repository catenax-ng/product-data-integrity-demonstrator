module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended'
  ],
  plugins: [
  ],
  // add your custom rules here
  rules: {
    indent: 'off',
    'vue/html-indent': 'off',
    'comma-dangle': 'off',
    camelcase: 0,
    'object-shorthand': 0,
    'vue/multi-word-component-names': 0,
    'dot-notation': 0
  }
}
