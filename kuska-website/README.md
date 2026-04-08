# Kuska Autism Services Website

A modern, responsive website for Kuska Autism Services, providing ABA therapy in Bountiful & Draper, Utah.

## Overview

This website is modeled after the Aviation ABA site, featuring a clean, welcoming design that's perfect for an autism services provider. The site includes all key sections needed to inform families and encourage contact.

## Features

### Design & Layout
- **Modern, Professional Design**: Clean aesthetic with calming colors
- **Fully Responsive**: Mobile-first design that works on all devices
- **Smooth Animations**: Floating clouds, fade-in effects, and smooth transitions
- **Accessible Navigation**: Clear menu structure with smooth scrolling

### Key Sections

1. **Hero Section**
   - Eye-catching gradient background with animated cloud decorations
   - Prominent headline and subtitle
   - Contact form for lead generation

2. **About Section**
   - Welcome message and company mission
   - Image placeholder for family/children photos
   - Call-to-action button

3. **Services Section**
   - Four service offerings in a grid layout:
     - In-Home Therapy
     - Center-Based Services
     - School Support
     - Parent Training
   - Custom SVG icons for each service
   - Hover effects on cards

4. **Locations Section**
   - Information for both Bountiful and Draper centers
   - Contact details and hours
   - Visually distinct cards

5. **Insurance Section**
   - Information about accepted insurance
   - Call-to-action for benefit verification

6. **Testimonials Carousel**
   - Three rotating testimonials
   - Navigation arrows and indicator dots
   - Auto-advances every 6 seconds
   - Keyboard navigation support (arrow keys)

7. **FAQs Section**
   - Four common questions with answers
   - Easy-to-scan grid layout

8. **Contact Section**
   - Comprehensive contact form
   - Location selector dropdown
   - Contact details displayed
   - Form validation with visual feedback

9. **Footer**
   - Quick links navigation
   - Contact information
   - Copyright and privacy policy link

### Interactive Features

- **Mobile Menu**: Hamburger menu with smooth animations
- **Smooth Scrolling**: Navigation links scroll smoothly to sections
- **Form Validation**: Real-time validation with color feedback
- **Phone Formatting**: Automatic phone number formatting
- **Scroll Animations**: Elements fade in as you scroll
- **Carousel**: Auto-advancing testimonial slider with manual controls

## File Structure

```
kuska-website/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # All styling and responsive design
├── js/
│   └── script.js       # Interactive features and functionality
├── images/             # Placeholder for images
└── README.md          # This file
```

## Customization Guide

### Colors
The color scheme can be adjusted in the CSS variables at the top of `style.css`:
- `--primary-color`: Main brand color (currently blue)
- `--secondary-color`: Accent color (currently purple)
- `--accent-color`: Success/highlight color (currently green)

### Content
To customize content, edit `index.html`:
- Replace placeholder addresses in the Locations section
- Update phone numbers and email addresses
- Modify service descriptions
- Add real testimonials
- Update FAQs based on actual questions

### Images
Add images to the `/images` folder and update references:
- Replace the SVG placeholder in the About section
- Add a logo to replace the text-based logo
- Add service icons if desired
- Include team photos or facility images

### Forms
The forms currently log data to the console. To make them functional:
1. Set up a backend endpoint to receive form submissions
2. Update the form submission handlers in `script.js`
3. Consider adding a service like Formspree, Netlify Forms, or your own API

## Browser Compatibility

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Deployment

This is a static website that can be deployed to:
- **Netlify**: Drag and drop deployment
- **Vercel**: GitHub integration
- **GitHub Pages**: Free hosting
- **Traditional hosting**: Upload via FTP to any web server

## Next Steps

1. **Add Real Content**: Replace placeholder text with actual information
2. **Add Images**: Include professional photos of staff, facilities, and happy families
3. **Set Up Forms**: Connect forms to an email service or CRM
4. **SEO Optimization**: Add meta tags, alt text, and structured data
5. **Analytics**: Add Google Analytics or similar tracking
6. **Accessibility**: Test with screen readers and add ARIA labels where needed
7. **Domain**: Point kuska.co to the deployed website

## Technologies Used

- HTML5
- CSS3 (with CSS Grid and Flexbox)
- Vanilla JavaScript (no frameworks)
- Google Fonts (Montserrat & Open Sans)

## Credits

Design inspired by Aviation ABA (aviationaba.com)
Built for Kuska Autism Services
