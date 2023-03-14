import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: <span>CaseStack</span>,
  project: {
    //link: 'https://github.com/shuding/nextra-docs-template',
  },
  chat: {
    //link: 'https://discord.com',
  },
  docsRepositoryBase: 'https://github.com/JonathanX64/everyfruitcase',
  footer: {
    //text: ' with love, \n Jonathunky',
  },
  sidebar: {
    defaultMenuCollapseLevel: 1
  },
  gitTimestamp: false,
  faviconGlyph: '🤙🏻',
  useNextSeoProps() {
    return {
      titleTemplate: '%s – CaseStack'
    }
  },
  toc: {
    float: true
  },
  head: function Head() {
    return (
      <>
        <meta name="robots" content="noindex" />
      </>
    );
  },
  search: {
    placeholder: "Search..."
  },
}

export default config
