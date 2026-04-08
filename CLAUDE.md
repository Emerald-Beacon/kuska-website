# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kuska Autism Services website - a static marketing website for ABA therapy services in Bountiful & Draper, Utah. Built with vanilla HTML, CSS, and JavaScript (no frameworks or build tools).

## Running the Site

Open `kuska-website/index.html` directly in a browser, or use a local server:
```bash
cd kuska-website && python3 -m http.server 8000
```

## Architecture

### File Structure
```
kuska-website/
├── index.html          # Single-page site with all sections
├── css/style.css       # All styles including responsive design
├── js/script.js        # Interactive features
└── images/             # Logo and image assets
```

### CSS Variables (style.css :root)
Brand colors are defined as CSS custom properties:
- `--primary-color: #3989c9` (Kuska Blue)
- `--secondary-color: #ebc94e` (Kuska Yellow)
- `--primary-dark: #004e85` / `--primary-light: #b7d9f3`

### Key JavaScript Features (script.js)
- **Mobile menu**: Hamburger toggle with CSS class `.active` on `.nav-menu`
- **Testimonials carousel**: Auto-advances every 6 seconds, supports keyboard arrows
- **Form handling**: Forms log to console (no backend) - see `hero-contact-form` and `contact-form` IDs
- **Scroll animations**: Uses IntersectionObserver for fade-in effects on cards/sections
- **Hidden editor**: Click footer logo 6 times to reveal a mock Claude Code editor interface

### Section Wave Transitions
Each section uses SVG wave patterns via `::after` pseudo-elements for smooth visual transitions between backgrounds. When modifying section backgrounds, update the corresponding wave fill color.

### Responsive Breakpoints
- 1024px: Services grid switches to 2 columns
- 768px: Mobile menu activates, single-column layouts
- 480px: Further size reductions for small screens

## Forms

Both contact forms (`#hero-contact-form` and `#contact-form`) currently only log data to console. To make functional, update the submit handlers in `script.js` to integrate with a backend service (Formspree, Netlify Forms, or custom API).
