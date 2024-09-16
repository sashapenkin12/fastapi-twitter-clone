module.exports = {
    env: {
      browser: true,
      node: true,
      es6: true
      // 'jest/globals': true
    },
    extends: ['plugin:vue/recommended', 'eslint:recommended'],
    rules: {
      'no-debugger': 'warn',
    }
    // plugins: ['jest'],
}