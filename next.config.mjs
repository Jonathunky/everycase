import nextra from "nextra";
import remarkMdxDisableExplicitJsx from "remark-mdx-disable-explicit-jsx";
import withPWA from "next-pwa";

const withNextra = nextra({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.tsx",
  mdxOptions: {
    remarkPlugins: [
      [
        remarkMdxDisableExplicitJsx,
        //{ whiteList: ["table", "thead", "tbody", "tr", "th", "td", "img"] },
      ],
    ],
  },
  // Additional options based on the template
  latex: true,
  flexsearch: {
    codeblocks: false,
  },
  defaultShowCopyCode: true,
});

const baseConfig = {
  images: {
    domains: ["applecase.wiki"],
    unoptimized: false,
  },
  swcMinify: true,
  reactStrictMode: true,
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  redirects: () => [
    {
      source: "/docs/guide/:slug(typescript|latex|tailwind-css|mermaid)",
      destination: "/docs/guide/advanced/:slug",
      permanent: true,
    },
    {
      source: "/docs/docs-theme/built-ins/:slug(callout|steps|tabs)",
      destination: "/docs/guide/built-ins/:slug",
      permanent: true,
    },
  ],
  webpack(config) {
    return config;
  },
};

const pwaConfig = {
  pwa: {
    dest: "public",
    disable: process.env.NODE_ENV === "development",
  },
};

export default withNextra(withPWA({ ...baseConfig, ...pwaConfig }));
