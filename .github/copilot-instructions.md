# Shop Sales & Profit Tracking System - Setup Instructions

This workspace contains a complete point-of-sale (POS) and inventory management system for retail shops.

## Project Overview

A Python + Streamlit + SQLite system that provides:
- Real-time sales dashboard
- Sales transaction entry form
- Stock/inventory management
- Profit calculations
- Daily/weekly/custom reports

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

- `app.py` - Main Streamlit application with all pages
- `database.py` - SQLite database operations
- `requirements.txt` - Python package dependencies
- `data/shop.db` - SQLite database (auto-created)
- `README.md` - Full documentation

## Pages Overview

1. **Dashboard** - KPIs, recent sales, stock status
2. **Add Sale** - Record transactions with profit calculation
3. **Manage Stock** - Add, update, delete products
4. **Reports** - Daily, weekly, and custom date range reports

## Key Features

✅ Automatic stock deduction on sales
✅ Real-time profit calculation
✅ Multiple payment methods
✅ Price override capability
✅ Profit margin display
✅ Complete transaction history
✅ Inventory tracking

## Database Schema

The system uses three main tables:
- `products` - Inventory items with pricing
- `sales` - Transaction records with profit data
- `daily_summary` - Daily KPI summaries

## Development Notes

- SQLite database is stored in `data/shop.db`
- No authentication required (designed for single shop use)
- Uses Streamlit's built-in session state for UI
- All calculations use KES currency (easily customizable)

## Usage Tips

1. Add all products before starting sales
2. Check stock levels in dashboard
3. Use "Add Sale" for each transaction
4. Review reports for business insights
5. Backup database regularly

---

For detailed documentation, see README.md
