import globals from "globals";
import pluginVue from "eslint-plugin-vue";


export default [
  {
    ignores: [
      "node_modules/",
      "client/*_module/dist/"
    ]
  },
  {
    rules: {
      "semi": "error",
      "prefer-const": "error"
    }
  },
  {files: ["**/*.js", "start.js"], languageOptions: {sourceType: "commonjs"}},
  {languageOptions: {globals: {...globals.browser, ...globals.node}}},
  ...pluginVue.configs["flat/essential"],
];
