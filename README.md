# Lifeline — site público

Site estático (HTML + CSS puro, sem framework e sem JavaScript) com a
página inicial, política de privacidade, termos de uso e suporte do app
Lifeline: Backup & Restore (Shopify). Sem cookies, sem rastreamento.

Publicado via GitHub Pages: https://zagojav.github.io/lifeline/

| Página                | English         | Português            |
|------------------------|-----------------|-----------------------|
| Início                 | `index.html`    | `index-pt.html`       |
| Política de privacidade| `privacy.html`  | `privacidade.html`    |
| Termos de uso           | `terms.html`    | `termos.html`         |
| Suporte                 | `support.html`  | `suporte.html`        |
| Erro 404                | `404.html` (bilíngue) | |

`assets/` guarda os ícones (favicons, apple-touch-icon, manifest icons,
imagem Open Graph) gerados a partir de `assets/lifeline-icone-1200.png`
pelos scripts em `scripts/` (usam `sips` e o Chrome headless do macOS,
sem dependências novas). Para regenerar depois de trocar o ícone fonte:

```
sips -z <N> <N> assets/lifeline-icone-1200.png --out assets/icon-<N>.png
python3 scripts/make_favicon_ico.py favicon.ico assets/icon-16.png assets/icon-32.png
python3 scripts/to_webp.py assets/icon-112.png assets/icon-112.webp 0.85
```

Este repositório não contém código do app, só o site.
