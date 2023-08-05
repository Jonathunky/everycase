const withNextra = require("nextra")({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.tsx",
});

const nextConfig = {
  images: {
    domains: ["applecase.wiki"],
    //imageSizes: [16, 32, 48, 64, 96, 128, 256, 384, 768],
    disableStaticImages: false,
  },
};

module.exports = withNextra(nextConfig);
