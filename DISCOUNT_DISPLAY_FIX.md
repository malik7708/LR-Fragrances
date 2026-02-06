# Discount Display - Fixed ✅

## Changes Made

### 1. **cart.html** - Updated to show discount information

- Shows original price with strikethrough
- Displays discount percentage in gold color
- Shows discounted price per item
- Displays subtotal with gold highlighting

### 2. **checkout.html** - Updated order summary with discount details

- Shows original price (strikethrough)
- Displays discount percentage in gold
- Shows final discounted price per item
- Displays quantity separately
- Shows subtotal for each item

### 3. **order_confirmation.html** - Updated order items display

- Shows original price (strikethrough) for discounted items
- Displays discount percentage in gold color
- Shows final price after discount
- Shows quantity for each item
- Displays item total

### 4. **track_order.html** - Updated with discount information

- Shows original price (strikethrough) if discount exists
- Displays discount percentage in gold
- Shows quantity and final price
- Shows item subtotal

### 5. **app.py** - Updated track_order route

- Modified SQL query to fetch original product price and discount
- Passes product discount information to template

## Discount Display Format

All pages now consistently show:

```
Original Price: PKR [PRICE] (strikethrough)
[DISCOUNT]% OFF (in gold color)
Final Price: PKR [DISCOUNTED_PRICE]
Quantity: [QTY]
Subtotal: PKR [SUBTOTAL]
```

## Benefits

✅ Customers see what they're saving
✅ Shows transparency in pricing
✅ Consistent display across all pages
✅ Professional presentation with color coding
✅ Clear breakdown of original vs. discounted prices
