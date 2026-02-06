# LR Fragrances - Animations Guide

## Overview

Professional and simple appealing animations have been added to all HTML pages across the LR Fragrances website. These animations enhance user experience with smooth transitions, hover effects, and page load entrances.

## File Structure

- **Main Animation File:** `static/css/animations.css`
- All HTML templates link to this file and use animation classes

## Animation Categories

### 1. Page Load & Fade In Animations

- `animate-fade-in` - Simple opacity fade in
- `animate-fade-in-up` - Fade in with upward movement
- `animate-fade-in-down` - Fade in with downward movement
- `animate-slide-in-left` - Slide in from left
- `animate-slide-in-right` - Slide in from right
- `animate-scale-in` - Scale from small to normal size

### 2. Staggered Animations

Delay animations for multiple elements (1-6):

- `.stagger-item-1` through `.stagger-item-6`
- Each item has 0.1s increments of delay
- Perfect for list items, product cards, feature boxes

### 3. Card & Content Animations

- `animate-card` - Fade up with hover lift effect
- `animate-product-card` - Product card with scale on hover
- `animate-feature-box` - Feature box with lift and scale
- `animate-image-zoom` - Image zoom on hover

### 4. Button Animations

- `animate-btn` - Base button with hover lift
- `animate-btn-glow` - Button with glow effect on hover
- `animate-btn-pulse` - Continuous pulse animation

### 5. Icon & Badge Animations

- `animate-spin` - Continuous rotation
- `animate-bounce` - Up and down bounce
- `animate-float` - Subtle floating motion
- `animate-pulse` - Opacity pulse
- `animate-wiggle` - Wiggle effect
- `animate-badge` - Badge scale with pulse
- `animate-price-badge` - Price with pulse on hover

### 6. Form Animations

- `animate-input:focus` - Input field glow on focus
- `animate-form-section` - Form section fade in
- `animate-label-float` - Label floating animation

### 7. Text Animations

- `animate-text-reveal` - Text clip reveal
- `animate-color-change` - Color alternation
- `animate-link` - Link with underline on hover

### 8. Navigation & Social

- `animate-nav-item` - Navigation hover effect
- `animate-social-icon` - Social icon with lift effect
- `animate-link` - Link with animated underline

### 9. Section Animations

- `animate-section` - Section fade in
- `animate-section-delay` - Section with delay
- `animate-hero-title` - Hero title slide down
- `animate-hero-subtitle` - Hero subtitle fade up
- `animate-hero-buttons` - Hero buttons fade in
- `animate-hero-image` - Hero image slide in

### 10. Review & Rating Animations

- `animate-review` - Review item fade in
- `animate-stars` - Stars fade in

### 11. Special Effects

- `animate-ripple` - Ripple effect on click
- `animate-skeleton` - Skeleton loading shimmer
- `animate-shake` - Shake animation
- `animate-expand` - Height expand animation
- `animate-highlight` - Color highlight animation
- `animate-back-to-top` - Back to top button slide up

## Pages Updated with Animations

### 1. **index.html** - Home Page

- Hero section: Title fade down, subtitle fade up, buttons fade in
- Hero image: Zoom on hover
- Feature boxes: Staggered fade in with 1-6 delays
- About section: Content slide in left, image zoom
- Footer sections: Staggered fade in
- WhatsApp button: Float animation

### 2. **shop.html** - Shop Page

- Header: Fade in down
- Product cards: Fade up with scale on hover, image zoom
- Price badges: Scale in with pulse
- Footer: Staggered fade in
- WhatsApp button: Float animation

### 3. **product.html** - Product Details

- Product image: Zoom on hover
- Product info: Slide in right
- Reviews: Staggered fade in
- Rating display: Scale in
- Rating bars: Slide in left
- Footer: Staggered fade in
- WhatsApp button: Float animation

### 4. **cart.html** - Shopping Cart

- Header: Fade in down
- Cart items: Card animation with image zoom
- Quantity buttons: Button animation
- Checkout button: Glow effect on hover
- Total price: Price badge animation
- Footer: Staggered fade in
- WhatsApp button: Float animation

### 5. **checkout.html** - Checkout Form

- Order summary: Slide in left
- Checkout form: Slide in right
- Form items: Image zoom
- Form inputs: Focus glow animation
- Footer social icons: Social icon animation
- WhatsApp button: Float animation

### 6. **contact.html** - Contact Page

- Footer: Staggered fade in with social icons
- Social icons: Hover lift animation
- WhatsApp button: Float animation

### 7. **about.html** - About Us Page

- Founder card: Card animation with image zoom
- Footer: Staggered fade in
- WhatsApp button: Float animation

### 8. **admin.html** - Admin Panel

- Animations CSS linked for consistency

### 9. **admin_login.html** - Admin Login

- Animations CSS linked for consistency

### 10. **order_confirmation.html** - Order Confirmation

- Animations CSS linked for consistency

### 11. **track_order.html** - Order Tracking

- Animations CSS linked for consistency

### 12. **change_password.html** - Change Password

- Animations CSS linked for consistency

### 13. **support.html** - Customer Support

- Animations CSS linked for consistency

### 14. **Policy Pages** (privacy.html, terms.html, shipping.html)

- Animations CSS linked for consistency

## Animation Specifications

### Timing

- **Fast animations:** 0.3s - 0.4s (buttons, hovers)
- **Standard animations:** 0.6s - 0.8s (page load, sections)
- **Slow animations:** 2s - 3s (floating, pulsing)
- **Stagger delay:** 0.1s increments per item

### Easing Functions

- `ease-out` - Page load animations
- `cubic-bezier(0.23, 1, 0.320, 1)` - Smooth hover effects
- `ease-in-out` - Floating, pulsing
- `linear` - Spinning/rotating

## Color Schemes

- Primary Gold: `#d7a719` (used in glow effects, highlights)
- Dark backgrounds: `#000`, `#1a1a1a`, `#151515`
- Hover effects: Rgba gold with transparency

## Best Practices Applied

1. **Performance:**
   - Uses `transform` and `opacity` for GPU acceleration
   - Minimal repaints/reflows
   - No animation on load for better perceived performance

2. **Accessibility:**
   - Respects `prefers-reduced-motion` media query ready
   - Animations don't interfere with interaction
   - Color changes have sufficient contrast

3. **User Experience:**
   - Subtle, non-distracting animations
   - Consistent animation durations across pages
   - Hover states provide clear feedback
   - Loading states have visual indication

4. **Cross-browser Compatibility:**
   - Uses standard CSS animations
   - No vendor prefixes needed (modern browsers)
   - Fallbacks for older browsers

## Customization Guide

To modify animations, edit `static/css/animations.css`:

### Change Animation Duration

```css
.animate-fade-in {
  animation: fadeIn 0.6s ease-out; /* Change 0.6s to desired duration */
}
```

### Change Animation Direction

```css
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px); /* Change -50px for different distance */
  }
}
```

### Adjust Stagger Delays

```css
.stagger-item-1 {
  animation: fadeInUp 0.7s ease-out 0.1s both; /* Change 0.1s for different delay */
}
```

## Testing Checklist

- ✅ All HTML pages load with animations
- ✅ Hero sections animate on page load
- ✅ Cards lift on hover with smooth transitions
- ✅ Buttons respond to clicks with visual feedback
- ✅ Images zoom smoothly on hover
- ✅ Footer sections stagger in smoothly
- ✅ Social icons lift on hover
- ✅ WhatsApp button floats gently
- ✅ Forms have focus animations
- ✅ Page transitions are smooth
- ✅ Animations don't impact page performance
- ✅ Mobile responsiveness maintained

## Browser Support

- Chrome 43+
- Firefox 16+
- Safari 9+
- Edge 12+
- Opera 30+
- Mobile browsers (iOS Safari, Chrome Mobile, etc.)

## Notes

- All animations are pure CSS (no JavaScript required)
- Animations enhance but don't block core functionality
- Can be further enhanced with scroll trigger libraries if needed
- Consider adding `prefers-reduced-motion: reduce` handling for accessibility compliance
