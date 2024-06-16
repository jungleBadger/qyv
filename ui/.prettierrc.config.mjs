export default {
  semi: true,
  singleQuote: false,
  trailingComma: "none",
  printWidth: 80,
  tabWidth: 2,
  useTabs: false,
  endOfLine: "lf",
  quoteProps: "as-needed",
  bracketSpacing: true,
  jsxBracketSameLine: false,
  arrowParens: "always",
  proseWrap: "preserve",
  htmlWhitespaceSensitivity: "css",
  vueIndentScriptAndStyle: false,
  insertPragma: false,
  requirePragma: false,
  embeddedLanguageFormatting: "auto",
  overrides: [
    {
      files: "*.json",
      options: {
        parser: "json",
        singleQuote: false,
        trailingComma: "none",
        tabWidth: 2
      }
    }
  ]
};
