import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'
import { useConfig } from 'nextra-theme-docs'
import { useRouter } from 'next/router'

const config: DocsThemeConfig = {
  logo: (
    <>
      <img
        src="/icon.png"
        alt="EveryCase Logo"
        style={{
          marginRight: '8px', width: '40px', height: 'auto'
        }}
        className="logo"
      />
      <span
        style={{
          fontFamily: 'Helvetica Neue',
          //fontWeight: 'bold',
          fontSize: '26px',
          letterSpacing: '0px',
          //color: '#333'
        }}
      >EveryCase</span>
    </>
  ),
  project: {
    // github link; will spawn it in the title bar
    //link: 'https://github.com/JonathanX64/everyfruitcase',
  },
  chat: {
    //link: 'https://discord.com',
  },
  docsRepositoryBase: 'https://github.com/JonathanX64/everyfruitcase',
  footer: {
    //text: "Yeah",
    component: undefined
  },
  sidebar: {
    defaultMenuCollapseLevel: 1,
    toggleButton: true
  },
  gitTimestamp: () => <></>,
  primaryHue: 320,
  useNextSeoProps() {
    const { asPath } = useRouter()
    const titleTemplate = asPath !== '/' ? '%s – EveryCase' : 'EveryCase';
    return {
      titleTemplate
    };
  },
  toc: {
    float: true,
    backToTop: true
  },
  feedback: {
    content: "Have something to add?"
  },
  editLink: {
    component: undefined
  },
  head: function Head() {
    const { title } = useConfig()

    return (
      <>
        <link rel="icon" href="/icon.png" type="image/png" sizes="64x64" />

        <meta name="robots" content="noindex" />
        <meta
          name="og:title"
          content={title ? title : 'EveryCase'}
        />
        <link rel="manifest" href="/manifest.json" />
        <meta name="application-name" content="next PWA demo" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="PWA App" />
        <meta name="description" content="Best PWA App in the world" />
        <meta name="format-detection" content="telephone=no" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="msapplication-config" content="none" /> {/* learn more  https://blog.giantgeek.com/?p=1418 */}
        <meta name="msapplication-TileColor" content="#FFE0F5" />
        <meta name="msapplication-tap-highlight" content="no" />
        <meta name="theme-color" content="#BF4F95" />
        <meta property="og:description" content="The website about Apple cases" />
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
    placeholder: "Search..."
  },
}

export default config