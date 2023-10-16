import React from "react";
import type { DocsThemeConfig } from "nextra-theme-docs";
import { useConfig } from "nextra-theme-docs";
import { useRouter } from "next/router";

const logo = (
  <>
    <picture>
      <img
        src="/icons/icon-512x512.png"
        alt="EveryCase Logo"
        className="logo"
      />
    </picture>
    <span
      style={{
        fontFamily: '"Quicksand", "Helvetica Neue", "Roboto", "Arimo", sans-serif',
        fontSize: "26px",
        letterSpacing: "0px",
        fontWeight: 300
      }}
    >
      EveryCase
    </span>
  </>
);

const config: DocsThemeConfig = {
  project: {
    // GitHub link; will spawn it in the title bar
    // link: 'https://github.com/JonathanX64/everyfruitcase',
  },
  chat: {
    //link: 'https://discord.com',
  },
  logo,
  docsRepositoryBase: "https://github.com/Jonathunky/everyfruitcase/tree/main/",
  footer: {
    //text: "Yeah",
    component: undefined,
  },
  sidebar: {
    titleComponent({ title, type }) {
      if (type === "separator") {
        return <span className="cursor-default">{title}</span>;
      }
      return <>{title}</>;
    },
    defaultMenuCollapseLevel: 2,
    toggleButton: true,
    autoCollapse: true
  },
  //gitTimestamp: () => <></>,
  darkMode: true,
  nextThemes: {
    defaultTheme: 'system'
  },
  primaryHue: 320,
  useNextSeoProps() {
    const { asPath } = useRouter();
    const titleTemplate = asPath !== "/" ? "%s – EveryCase" : "EveryCase";
    return {
      titleTemplate,
      noindex: true,
      nofollow: true,
      dangerouslySetAllPagesToNoFollow: true,
      dangerouslySetAllPagesToNoIndex: true
    };
  },
  toc: {
    float: true,
    backToTop: true,
  },
  feedback: {
    content: "Leave feedback →",
  },
  editLink: {
    text: "Propose edits on GitHub →",
  },
  navigation: {
    prev: false,
    next: false
  },
  head: function Head() {
    const { title } = useConfig();
    const router = useRouter();

    const baseURL = "https://applecase.wiki";
    const currentURL = `${baseURL}${router.asPath}`;

    return (
      <>
        {/* Basic Information */}
        <link rel="icon" href="/icons/android-chrome-512x512.png" type="image/png" sizes="512x512" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#BF4F95" />
        <meta name="application-name" content="EveryCase" />
        <meta name="description" content="Library of Apple cases for iPhone, iPad, and Mac." />

        {/* OpenGraph Tags */}
        <meta property="og:type" content="website" />
        {/* <meta property="og:title" content={title ? title : "EveryCase"} /> — managed by NextSeo plugin*/}

        <meta property="og:description" content="Library of Apple cases for iPhone, iPad, and Mac." />
        <meta property="og:image" content="https://applecase.wiki/icons/back.jpg" />
        <meta property="og:url" content={currentURL} />
        <meta property="og:locale" content="en_GB" />

        {/* Twitter Tags */}
        <meta property="twitter:image" content="https://applecase.wiki/icons/back.jpg" />
        <meta name="twitter:card" content="summary" />
        <meta property="twitter:title" content={title ? title : "EveryCase"} />
        <meta property="twitter:description" content="Library of Apple cases for iPhone, iPad, and Mac." />

        {/* Apple Specific Tags */}
        <meta name="apple-mobile-web-app-title" content="EveryCase" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png" />
        <link rel="mask-icon" href="/icons/safari-pinned-tab.svg" color="#bf4f95" />

        {/* Microsoft Specific Tags */}
        <meta name="msapplication-config" content="none" />
        <meta name="msapplication-TileColor" content="#FFE0F5" />
        <meta name="msapplication-tap-highlight" content="no" />

        {/* Miscellaneous */}
        {/* <meta name="robots" content="noindex" /> also managed by plugin */}
        <meta name="format-detection" content="telephone=no" />
        <meta name="mobile-web-app-capable" content="yes" />
      </>
    );
  },
  search: {
    placeholder: "Search...",
  },
};

export default config;
