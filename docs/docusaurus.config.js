// @ts-check

import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'WORDWISE',
  tagline: 'Sua plataforma de e-commerce de livros',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://seusite.com',
  baseUrl: '/',

  organizationName: 'larissa-ferrari', // troque pelo seu usuário ou org no GitHub
  projectName: 'wordwise-store', // troque pelo nome do seu repositório

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/larissa-ferrari/wordwise-store/edit/main/docs/',
        },
        blog: false, 
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/wordwise-social-card.jpg',
      navbar: {
        title: 'WORDWISE',
        logo: {
          alt: 'Logo Wordwise',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Documentação',
          },
          {
            href: 'https://github.com/larissa-ferrari/wordwise-store',
            label: 'GitHub',
            position: 'right',
          },
          {
            href: 'http://localhost:3000',
            label: 'Ver Plataforma',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentação',
            items: [
              {
                label: 'Visão Geral',
                to: '/docs/overview',
              },
              {
                label: 'Tecnologias',
                to: '/docs/technologies',
              },
              {
                label: 'Módulos',
                to: '/docs/modules',
              },
            ],
          },
          {
            title: 'Mais',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/SEU_USUARIO_GITHUB/wordwise',
              },
              {
                label: 'Contato',
                href: 'mailto:seuemail@dominio.com',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} WORDWISE.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
