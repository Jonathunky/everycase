import React from "react";
import Image from "next/image";
import type { DocsThemeConfig } from "nextra-theme-docs";
import { useConfig } from "nextra-theme-docs";
import { useRouter } from "next/router";

const logo = (
  <>
    <Image
      src="/icon.png"
      alt="EveryCase Logo"
      width={40}
      height={40} // Adjust this according to the aspect ratio of your image
      className="logo"
      //layout="fixed"
      quality={100}
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
  docsRepositoryBase: "https://github.com/JonathanX64/everyfruitcase/tree/main/",
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
        <link rel="icon" href="/icon.png" type="image/png" sizes="64x64" />
        <meta name="robots" content="noindex" />
        <meta name="og:title" content={title ? title : "EveryCase"} />
        <link rel="manifest" href="/manifest.json" />
        <meta name="application-name" content="next PWA demo" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="PWA App" />
        <meta name="description" content="Best PWA App in the world" />
        <meta name="format-detection" content="telephone=no" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="msapplication-config" content="none" />{" "}
        {/* learn more  https://blog.giantgeek.com/?p=1418 */}
        <meta name="msapplication-TileColor" content="#FFE0F5" />
        <meta name="msapplication-tap-highlight" content="no" />
        <meta name="theme-color" content="#BF4F95" />
        <meta
          property="og:description"
          content="The website about Apple cases"
        />
        <style>
          {`
            @font-face {
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
              font-style: normal;
              font-weight: 400;
            }
          `}
        </style>
      </>
    );
  },
  search: {
    placeholder: "Search...",
  },
};

export default config;
