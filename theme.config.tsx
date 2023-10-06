import React from "react";
import Image from "next/image";
import type { DocsThemeConfig } from "nextra-theme-docs";
import { useConfig } from "nextra-theme-docs";
import { useRouter } from "next/router";

const logo = (
  <>
    <img
      src="/icons/icon-512x512.png"
      alt="EveryCase Logo"
      className="logo"
    />
    <span
      style={{
        fontFamily: '"Helvetica Neue", "Roboto", "Arimo", sans-serif',
        fontSize: "26px",
        letterSpacing: "0px",
      }}
    >
      EveryCase
    </span>
  </>
);

const config: DocsThemeConfig = {
  project: {
    // github link; will spawn it in the title bar
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
    defaultMenuCollapseLevel: 1,
    toggleButton: true,
  },
  gitTimestamp: () => <></>,
  primaryHue: 320,
  useNextSeoProps() {
    const { asPath } = useRouter();
    const titleTemplate = asPath !== "/" ? "%s – EveryCase" : "EveryCase";
    return {
      titleTemplate,
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
  head: function Head() {
    const { title } = useConfig();

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
        <meta property="og:title" content={title ? title : "EveryCase"} />
        <meta property="og:description" content="Library of Apple cases for iPhone, iPad, and Mac." />
        <meta property="og:image" content="/icons/icon.png" />

        {/* Apple Specific Tags */}
        <meta name="apple-mobile-web-app-title" content="EveryCase" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="mask-icon" href="/icons/safari-pinned-tab.svg" color="#bf4f95" />

        {/* Microsoft Specific Tags */}
        <meta name="msapplication-config" content="none" />
        <meta name="msapplication-TileColor" content="#FFE0F5" />
        <meta name="msapplication-tap-highlight" content="no" />

        {/* Miscellaneous */}
        <meta name="robots" content="noindex" /> {/* until it's ready */}
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
