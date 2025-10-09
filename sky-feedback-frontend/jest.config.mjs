/**
 * For a detailed explanation regarding each configuration property, visit:
 * https://jestjs.io/docs/configuration
 */

/** @type {import('jest').Config} */
const config = {
  // other settings...
  transform: {
    "^.+\\.[tj]sx?$": "babel-jest",
  },
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/components/__tests__/setup.js"], // optional
  moduleNameMapper: {
    "\\.(jpg|jpeg|png|gif|webp|svg)$":
      "<rootDir>/src/components/__mocks__/fileMock.js",
    "\\.(css|less|scss)$": "identity-obj-proxy",
  },
};

export default config;
