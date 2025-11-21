# Sample Customers for Testing

This document lists all available sample customers and their orders for testing the RRVA system.

## Customer List

### CUST-001: Sanjyot Sathe
- **Email**: sanjyot.sathe@gmail.com
- **Phone**: +1-555-0123
- **Name**: Sanjyot Sathe
- **Orders**: ORD-001, ORD-002, ORD-004
- **Last 4 Digits**: 4532

**Orders:**
- **ORD-001**: Wireless Headphones + USB-C Cable ($149.99) - Jan 15, 2025
- **ORD-002**: Phone Case ($79.99) - Feb 1, 2025 (used condition)
- **ORD-004**: Bluetooth Speaker ($199.99) - Feb 10, 2025

---

### CUST-002: Sarah Johnson
- **Email**: sarah.johnson@gmail.com
- **Phone**: +1-555-0456
- **Name**: Sarah Johnson
- **Orders**: ORD-003, ORD-005
- **Last 4 Digits**: 7891

**Orders:**
- **ORD-003**: Smart Watch ($299.99) - Jan 20, 2025
- **ORD-005**: Wireless Mouse ($89.99) - Jan 25, 2025

---

### CUST-003: David Rodriguez
- **Email**: david.rodriguez@outlook.com
- **Phone**: +1-555-0789
- **Name**: David Rodriguez
- **Orders**: ORD-006, ORD-007
- **Last 4 Digits**: 2345

**Orders:**
- **ORD-006**: Gaming Keyboard ($349.99) - Jan 18, 2025
- **ORD-007**: Webcam HD ($129.99) - Feb 5, 2025

---

### CUST-004: Emily Williams
- **Email**: emily.williams@yahoo.com
- **Phone**: +1-555-0321
- **Name**: Emily Williams
- **Orders**: ORD-008
- **Last 4 Digits**: 6789

**Orders:**
- **ORD-008**: Tablet Stand ($249.99) - Jan 22, 2025

---

### CUST-005: James Brown
- **Email**: james.brown@email.com
- **Phone**: +1-555-0654
- **Name**: James Brown
- **Orders**: ORD-009, ORD-010, ORD-011
- **Last 4 Digits**: 1234

**Orders:**
- **ORD-009**: Portable Charger ($179.99) - Jan 12, 2025
- **ORD-010**: Screen Protector x2 ($59.99) - Jan 28, 2025
- **ORD-011**: Noise Cancelling Earbuds ($399.99) - Feb 8, 2025

---

### CUST-006: Jessica Martinez
- **Email**: jessica.martinez@hotmail.com
- **Phone**: +1-555-0987
- **Name**: Jessica Martinez
- **Orders**: ORD-012
- **Last 4 Digits**: 5678

**Orders:**
- **ORD-012**: USB Hub ($159.99) - Jan 30, 2025

---

### CUST-007: Robert Taylor
- **Email**: robert.taylor@gmail.com
- **Phone**: +1-555-0147
- **Name**: Robert Taylor
- **Orders**: ORD-013, ORD-014
- **Last 4 Digits**: 9012

**Orders:**
- **ORD-013**: External Hard Drive ($219.99) - Feb 3, 2025
- **ORD-014**: Laptop Sleeve ($69.99) - Feb 12, 2025

---

### CUST-008: Amanda Anderson
- **Email**: amanda.anderson@email.com
- **Phone**: +1-555-0258
- **Name**: Amanda Anderson
- **Orders**: ORD-015
- **Last 4 Digits**: 3456

**Orders:**
- **ORD-015**: Monitor Stand ($279.99) - Jan 26, 2025

---

### CUST-009: Ryan Thompson
- **Email**: ryan.thompson@gmail.com
- **Phone**: +1-555-0369
- **Name**: Ryan Thompson
- **Orders**: ORD-016, ORD-017
- **Last 4 Digits**: 4567

**Orders:**
- **ORD-016**: Mechanical Keyboard ($189.99) - Feb 5, 2025 ✅ **Within refund window**
- **ORD-017**: Wireless Charging Pad ($119.99) - Nov 8, 2025 ✅ **Within refund window**

---

### CUST-010: Lisa Garcia
- **Email**: lisa.garcia@yahoo.com
- **Phone**: +1-555-0741
- **Name**: Lisa Garcia
- **Orders**: ORD-018
- **Last 4 Digits**: 8901

**Orders:**
- **ORD-018**: Smart Home Hub ($259.99) - Feb 3, 2025 ✅ **Within refund window**

---

### CUST-011: Christopher Lee
- **Email**: christopher.lee@email.com
- **Phone**: +1-555-0852
- **Name**: Christopher Lee
- **Orders**: ORD-019, ORD-020
- **Last 4 Digits**: 2345

**Orders:**
- **ORD-019**: USB-C Dock ($139.99) - Feb 6, 2025 ✅ **Within refund window**
- **ORD-020**: Laptop Stand Adjustable ($89.99) - Feb 10, 2025 ✅ **Within refund window**

---

### CUST-012: Nicole White
- **Email**: nicole.white@outlook.com
- **Phone**: +1-555-0963
- **Name**: Nicole White
- **Orders**: ORD-021
- **Last 4 Digits**: 6789

**Orders:**
- **ORD-021**: 4K Webcam ($329.99) - Feb 7, 2025 ✅ **Within refund window**

---

### CUST-013: Kevin Harris
- **Email**: kevin.harris@hotmail.com
- **Phone**: +1-555-0147
- **Name**: Kevin Harris
- **Orders**: ORD-022
- **Last 4 Digits**: 0123

**Orders:**
- **ORD-022**: Ergonomic Mouse ($199.99) - Feb 9, 2025 ✅ **Within refund window**

---

### CUST-014: Rachel Clark
- **Email**: rachel.clark@gmail.com
- **Phone**: +1-555-0258
- **Name**: Rachel Clark
- **Orders**: ORD-023, ORD-024
- **Last 4 Digits**: 7890

**Orders:**
- **ORD-023**: Wireless Earbuds Pro ($149.99) - Feb 4, 2025 ✅ **Within refund window**
- **ORD-024**: Phone Stand with Charger ($79.99) - Feb 11, 2025 ✅ **Within refund window**

---

## Verification Method

**Email-only verification** - No OTP required.

To verify a customer:
1. Provide order ID
2. Provide email address matching the customer's registered email
3. Verification succeeds if email matches

## Test Scenarios

### Scenario 1: Eligible Refund (Within 30 Days)
- **Customer**: Sanjyot Sathe
- **Order**: ORD-001 ($149.99, Jan 15, 2025)
- **Email**: sanjyot.sathe@gmail.com
- **Status**: ✅ Eligible (within 30-day window, unopened items)

### Scenario 2: Partial Refund (Used Item)
- **Customer**: Sanjyot Sathe
- **Order**: ORD-002 ($79.99, Feb 1, 2025)
- **Email**: sanjyot.sathe@gmail.com
- **Status**: ⚠️ Partial eligible (used condition, restocking fee applies)

### Scenario 3: High-Value Refund
- **Customer**: Sarah Johnson
- **Order**: ORD-003 ($299.99, Jan 20, 2025)
- **Email**: sarah.johnson@gmail.com
- **Status**: ✅ Eligible

### Scenario 4: Multiple Orders Customer
- **Customer**: James Brown
- **Orders**: ORD-009, ORD-010, ORD-011
- **Email**: james.brown@email.com
- **Test**: Verify customer can see all their orders

### Scenario 5: Single Order Customer
- **Customer**: Emily Williams
- **Order**: ORD-008 ($249.99)
- **Email**: emily.williams@yahoo.com
- **Status**: ✅ Eligible

### Scenario 6: Recent Order - Within Refund Window
- **Customer**: Ryan Thompson
- **Order**: ORD-016 ($189.99, Feb 5, 2025)
- **Email**: ryan.thompson@gmail.com
- **Status**: ✅ Eligible (recent order, well within 30-day window)

### Scenario 7: Very Recent Order
- **Customer**: Rachel Clark
- **Order**: ORD-024 ($79.99, Feb 11, 2025)
- **Email**: rachel.clark@gmail.com
- **Status**: ✅ Eligible (very recent, definitely within window)

### Scenario 8: High-Value Recent Order
- **Customer**: Nicole White
- **Order**: ORD-021 ($329.99, Feb 7, 2025)
- **Email**: nicole.white@outlook.com
- **Status**: ✅ Eligible (high-value, recent order)

### Scenario 9: Multiple Recent Orders
- **Customer**: Christopher Lee
- **Orders**: ORD-019 ($139.99), ORD-020 ($89.99)
- **Email**: christopher.lee@email.com
- **Status**: ✅ Both eligible (recent orders)

## Quick Reference

| Customer ID | Name | Email | Order Count |
|------------|------|-------|-------------|
| CUST-001 | Sanjyot Sathe | sanjyot.sathe@gmail.com | 3 |
| CUST-002 | Sarah Johnson | sarah.johnson@gmail.com | 2 |
| CUST-003 | David Rodriguez | david.rodriguez@outlook.com | 2 |
| CUST-004 | Emily Williams | emily.williams@yahoo.com | 1 |
| CUST-005 | James Brown | james.brown@email.com | 3 |
| CUST-006 | Jessica Martinez | jessica.martinez@hotmail.com | 1 |
| CUST-007 | Robert Taylor | robert.taylor@gmail.com | 2 |
| CUST-008 | Amanda Anderson | amanda.anderson@email.com | 1 |
| CUST-009 | Ryan Thompson | ryan.thompson@gmail.com | 2 |
| CUST-010 | Lisa Garcia | lisa.garcia@yahoo.com | 1 |
| CUST-011 | Christopher Lee | christopher.lee@email.com | 2 |
| CUST-012 | Nicole White | nicole.white@outlook.com | 1 |
| CUST-013 | Kevin Harris | kevin.harris@hotmail.com | 1 |
| CUST-014 | Rachel Clark | rachel.clark@gmail.com | 2 |

## Testing Tips

1. **Use realistic names and emails** - All customers have proper names and email addresses
2. **Email verification only** - No need for OTP, just match the email
3. **Various order amounts** - Range from $59.99 to $399.99
4. **Different order dates** - Test 30-day window policy
5. **Mixed conditions** - Most items are unopened, ORD-002 is used
6. **Multiple orders per customer** - Test order history retrieval

