import js from "@eslint/js";
import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";

export default [
  { ignores: ["dist/**", "node_modules/**", "playwright-report/**", "test-results/**"] },
  js.configs.recommended,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser: tsParser,
      parserOptions: { ecmaFeatures: { jsx: true }, sourceType: "module" },
      globals: {
        AbortSignal: "readonly",
        AbortController: "readonly",
        RequestInit: "readonly",
        TextDecoder: "readonly",
        crypto: "readonly",
        document: "readonly",
        expect: "readonly",
        fetch: "readonly",
        navigator: "readonly",
        test: "readonly",
        window: "readonly",
      },
    },
    plugins: { "@typescript-eslint": tseslint, "react-hooks": reactHooks },
    rules: {
      ...tseslint.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
    },
  },
];
