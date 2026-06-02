# 🏪 Shop Sales & Profit Tracking System

A complete point-of-sale (POS) and inventory management system built with Python, Streamlit, and SQLite. Perfect for small retail shops and convenience stores.

## Features

✅ **Real-time Sales Dashboard**
- View today's sales, profit, and transaction count
- Monitor current stock status
- Track recent transactions

✅ **Sales Entry Form**
- Quick product selection with stock availability
- Automatic price and profit calculation
- Multiple payment method support (Cash, M-Pesa, Card, Credit)
- Instant sale recording with automatic stock deduction

✅ **Stock Management**
- Add new products with buying and selling prices
- Update existing product details and stock levels
- Automatic profit margin calculation
- Delete products from inventory

✅ **Comprehensive Reports**
- Daily sales summary
- Weekly performance analysis
- Custom date range reports
- Profit and sales metrics

## System Architecture

```
Data Flow:
Cashier Input (Sales Page)
        ↓
SQLite Database
        ↓
Business Logic (Calculations)
        ↓
Dashboard (Real-time Display)
```

## Database Schema

### Products Table
- `id` - Product ID
- `name` - Product name (unique)
- `category` - Product category
- `buying_price` - Cost price from supplier
- `selling_price` - Retail price
- `quantity` - Current stock level

### Sales Table
- `id` - Transaction ID
- `product_id` - Foreign key to products
- `product_name` - Product name at time of sale
- `quantity` - Items sold
- `unit_price` - Selling price per unit
- `total_amount` - Total sale amount
- `cost_price` - Cost price of sold items
- `profit` - Profit from transaction
- `payment_method` - Payment type
- `created_at` - Transaction timestamp

### Daily Summary Table
- `id` - Record ID
- `date` - Date of summary
- `total_sales` - Total revenue
- `total_profit` - Total profit
- `total_items_sold` - Number of items sold
- `transaction_count` - Number of transactions

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage Guide

### 1. Dashboard (Home Page)
- **Overview**: See KPIs at a glance
- **Recent Sales**: View transactions from today
- **Stock Status**: Check current inventory

### 2. Add Sale
1. Select product from dropdown (shows available stock)
2. Enter quantity sold
3. Choose payment method
4. System auto-calculates total and profit
5. Optional: Override selling price if needed
6. Click "Complete Sale"

### 3. Manage Stock
**Add New Product:**
- Enter product name, category
- Set buying and selling prices
- Add initial stock quantity
- System shows profit margin automatically

**Update Stock:**
- Select existing product
- Update prices, quantity, or category
- Changes apply immediately

**Delete Product:**
- Select product to remove
- Confirm deletion

### 4. Reports
**Daily Report:** Today's complete summary with KPIs

**Weekly Report:** Performance analysis from Monday to today

**Custom Date Range:** Generate reports for any period

## File Structure

```
shop_system/
├── app.py                 # Main Streamlit application
├── database.py            # Database operations and queries
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/
│   └── shop.db          # SQLite database (auto-created)
└── .github/
    └── copilot-instructions.md
```

## Key Functions

### Database Functions
- `init_db()` - Initialize database with tables
- `add_product()` - Add new product
- `get_all_products()` - Retrieve all products
- `add_sale()` - Record a sale transaction
- `reduce_stock()` - Decrease product quantity
- `get_today_sales()` - Get today's transactions
- `get_today_summary()` - Get daily KPIs
- `get_sales_by_date_range()` - Get report data

## Tips for Best Performance

1. **Regular Backups**: Periodically backup the `data/shop.db` file
2. **Stock Monitoring**: Check daily for low stock items
3. **Profit Analysis**: Review profit margins weekly
4. **Transaction Review**: Monitor payment methods used

## Troubleshooting

**Issue: Application won't start**
- Ensure Python 3.8+ is installed
- Run `pip install -r requirements.txt` again
- Check that port 8501 is not in use

**Issue: Database errors**
- Delete the `data/shop.db` file to reset the database
- Restart the application

**Issue: Sales not showing**
- Ensure products are added first
- Check that products have stock available
- Verify payment method is selected

## Future Enhancements

- User authentication (cashier logins)
- Multi-user support with role-based access
- Barcode scanning for faster sales entry
- Inventory alerts for low stock
- Export reports to PDF/Excel
- Product images
- Customer profiles and loyalty tracking
- Voice-based sales entry

## Support

For issues or feature requests, please check:
1. Product has been added to inventory
2. Stock quantity is sufficient
3. Prices are set correctly

## License

This system is built for educational and small business use.

---

**Built with ❤️ using Streamlit, Python, and SQLite**
