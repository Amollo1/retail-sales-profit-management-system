import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from database import get_today_summary, get_today_sales, get_all_products

# Page configuration
st.set_page_config(
    page_title="Omoga Shop Sales System",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .profit-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .sales-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🏪 Omoga B Shop System")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "💳 Add Sale", "📦 Manage Stock", "📋 Reports"]
)

# Main content
if page == "📊 Dashboard":
    st.title("📊 Daily Sales Dashboard")
    
    # Get today's summary
    summary = get_today_summary()
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Sales",
            value=f"KES {summary['total_sales']:.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="📈 Total Profit",
            value=f"KES {summary['total_profit']:.2f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="📦 Items Sold",
            value=f"{summary['total_items_sold']}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="🔔 Transactions",
            value=f"{summary['transaction_count']}",
            delta=None
        )
    
    st.divider()
    
    # Recent sales table
    st.subheader("📝 Recent Sales Today")
    sales_data = get_today_sales()
    
    if sales_data:
        sales_df = pd.DataFrame(sales_data, columns=[
            'ID', 'Product', 'Qty', 'Price', 'Total', 'Profit', 'Payment', 'Time'
        ])
        sales_df['Time'] = pd.to_datetime(sales_df['Time']).dt.strftime('%H:%M:%S')
        
        st.dataframe(
            sales_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                'ID': st.column_config.NumberColumn("ID", width="small"),
                'Product': st.column_config.TextColumn("Product Name", width="medium"),
                'Qty': st.column_config.NumberColumn("Quantity", width="small"),
                'Price': st.column_config.NumberColumn("Unit Price", format="KES %.2f", width="small"),
                'Total': st.column_config.NumberColumn("Total", format="KES %.2f", width="small"),
                'Profit': st.column_config.NumberColumn("Profit", format="KES %.2f", width="small"),
                'Payment': st.column_config.TextColumn("Payment Method", width="small"),
                'Time': st.column_config.TextColumn("Time", width="small"),
            }
        )
    else:
        st.info("No sales recorded today yet.")
    
    # Stock status
    st.divider()
    st.subheader("📦 Current Stock Status")
    products = get_all_products()
    
    if products:
        stock_df = pd.DataFrame(products, columns=[
            'ID', 'Product', 'Category', 'Buy Price', 'Sell Price', 'Quantity'
        ])
        
        st.dataframe(
            stock_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                'ID': st.column_config.NumberColumn("ID", width="small"),
                'Product': st.column_config.TextColumn("Product Name", width="medium"),
                'Category': st.column_config.TextColumn("Category", width="small"),
                'Buy Price': st.column_config.NumberColumn("Buy Price", format="KES %.2f", width="small"),
                'Sell Price': st.column_config.NumberColumn("Sell Price", format="KES %.2f", width="small"),
                'Quantity': st.column_config.NumberColumn("In Stock", width="small"),
            }
        )
    else:
        st.info("No products in inventory yet.")

elif page == "💳 Add Sale":
    st.title("💳 Shopping Cart - Multi-Item Transaction")
    
    # Initialize shopping cart in session state
    if 'shopping_cart' not in st.session_state:
        st.session_state.shopping_cart = []
    if 'payment_method' not in st.session_state:
        st.session_state.payment_method = "Cash"
    
    products = get_all_products()
    
    if not products:
        st.warning("No products in inventory. Please add products first in 'Manage Stock' section.")
    else:
        # Left column - Product selection
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("➕ Add Items to Cart")
            
            # Create product selection
            product_list = {f"{p[1]} ({p[5]} in stock)": p for p in products}
            selected_product_name = st.selectbox("Select Product", list(product_list.keys()), key="select_product_sales")
            selected_product = product_list[selected_product_name]
            
            product_id, product_name, category, buying_price, selling_price, available_qty = selected_product
            
            st.info(f"**Buy Price:** KES {buying_price:.2f} | **Sell Price:** KES {selling_price:.2f}")
            
            # Check if stock is available
            if available_qty <= 0:
                st.error(f"⚠️ Out of Stock! '{product_name}' has no available quantity.")
            else:
                # Input fields
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    quantity = st.number_input("Quantity", min_value=1, max_value=available_qty, value=1, key="qty_input")
                
                with col2:
                    price_override = st.checkbox("Override Price")
                    if price_override:
                        unit_price = st.number_input("Custom Price", value=float(selling_price), min_value=0.0, key="custom_price")
                    else:
                        unit_price = selling_price
                
                with col3:
                    # Calculate profit for display
                    profit_per_unit = unit_price - buying_price
                    st.metric("Profit/Unit", f"KES {profit_per_unit:.2f}")
                
                # Add to cart button
                if st.button("🛒 Add to Cart", type="primary", use_container_width=True):
                    # Check if product already in cart
                    cart_item_index = None
                    for i, item in enumerate(st.session_state.shopping_cart):
                        if item['product_id'] == product_id:
                            cart_item_index = i
                            break
                    
                    if cart_item_index is not None:
                        # Update quantity if product already in cart
                        st.session_state.shopping_cart[cart_item_index]['quantity'] += quantity
                        st.session_state.shopping_cart[cart_item_index]['total'] += quantity * unit_price
                        st.session_state.shopping_cart[cart_item_index]['total_profit'] += quantity * profit_per_unit
                    else:
                        # Add new item to cart
                        st.session_state.shopping_cart.append({
                            'product_id': product_id,
                            'product_name': product_name,
                            'category': category,
                            'buying_price': buying_price,
                            'selling_price': selling_price,
                            'quantity': quantity,
                            'unit_price': unit_price,
                            'total': quantity * unit_price,
                            'profit_per_unit': profit_per_unit,
                            'total_profit': quantity * profit_per_unit
                        })
                    
                    st.success(f"✅ Added {quantity}x {product_name} to cart!")
                    st.rerun()
        
        with col_right:
            st.subheader("🛍️ Cart Summary")
            
            if len(st.session_state.shopping_cart) == 0:
                st.info("Cart is empty. Add items from the left panel.")
            else:
                # Display cart items
                cart_data = []
                total_sale_amount = 0
                total_profit_amount = 0
                
                for idx, item in enumerate(st.session_state.shopping_cart):
                    cart_data.append({
                        'Product': item['product_name'],
                        'Qty': item['quantity'],
                        'Unit Price': f"KES {item['unit_price']:.2f}",
                        'Total': f"KES {item['total']:.2f}",
                        'Profit': f"KES {item['total_profit']:.2f}"
                    })
                    total_sale_amount += item['total']
                    total_profit_amount += item['total_profit']
                
                cart_df = pd.DataFrame(cart_data)
                st.dataframe(cart_df, use_container_width=True, hide_index=True)
                
                # Cart totals
                st.divider()
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Items", len(st.session_state.shopping_cart))
                with col2:
                    st.metric("Total Sale", f"KES {total_sale_amount:.2f}")
                with col3:
                    st.metric("Total Profit", f"KES {total_profit_amount:.2f}")
                
                st.divider()
        
        # Payment method selection and checkout
        if len(st.session_state.shopping_cart) > 0:
            st.divider()
            st.subheader("💰 Complete Transaction")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Use a local variable to capture the selectbox value (don't assign directly to session_state)
                payment_method = st.selectbox(
                    "Payment Method",
                    ["Cash", "M-Pesa", "Card", "Credit"],
                    index=["Cash", "M-Pesa", "Card", "Credit"].index(st.session_state.payment_method),
                    key="payment_method_select"
                )
            
            with col2:
                st.write("")  # spacing
                if st.button("🗑️ Clear Cart", use_container_width=True):
                    st.session_state.shopping_cart = []
                    st.rerun()
            
            # Final checkout button
            if st.button("✅ Finalize Transaction", type="primary", use_container_width=True, key="checkout_button"):
                from database import add_sale, reduce_stock
                
                try:
                    # Process each item in the cart
                    for item in st.session_state.shopping_cart:
                        add_sale(
                            item['product_id'],
                            item['product_name'],
                            item['quantity'],
                            item['unit_price'],
                            item['buying_price'],
                            payment_method
                        )
                        reduce_stock(item['product_id'], item['quantity'])
                    
                    # Calculate totals
                    transaction_total = sum(item['total'] for item in st.session_state.shopping_cart)
                    transaction_profit = sum(item['total_profit'] for item in st.session_state.shopping_cart)
                    items_count = len(st.session_state.shopping_cart)
                    
                    # Update session state with the payment method used
                    st.session_state.payment_method = payment_method
                    
                    # Clear the cart
                    st.session_state.shopping_cart = []
                    
                    # Show success message
                    st.success(f"""
                    ✅ Transaction Completed!
                    
                    📦 Items: {items_count} product(s)
                    💰 Total Sale: KES {transaction_total:.2f}
                    📈 Total Profit: KES {transaction_profit:.2f}
                    💳 Payment: {payment_method}
                    """)
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error completing transaction: {str(e)}")

elif page == "📦 Manage Stock":
    st.title("📦 Stock Management")
    
    tab1, tab2, tab3 = st.tabs(["Add New Product", "Update Stock", "View All Products"])
    
    with tab1:
        st.subheader("Add New Product")
        
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("Product Name", placeholder="e.g., Bread 400g")
            category = st.selectbox("Category", ["Groceries", "Dairy", "Beverages", "Household", "Other"], key="category_add_product")
        
        with col2:
            buying_price = st.number_input("Buying Price (KES)", min_value=0.0, step=0.50)
            selling_price = st.number_input("Selling Price (KES)", min_value=0.0, step=0.50)
        
        quantity = st.number_input("Initial Quantity", min_value=0, step=1)
        
        # Profit margin preview
        if buying_price > 0:
            margin = ((selling_price - buying_price) / buying_price) * 100
            st.info(f"Profit Margin: {margin:.1f}%")
        
        if st.button("➕ Add Product", use_container_width=True):
            from database import add_product
            if product_name and buying_price > 0 and selling_price > buying_price:
                success, message = add_product(product_name, category, buying_price, selling_price, quantity)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill all fields correctly. Selling price must be higher than buying price.")
    
    with tab2:
        st.subheader("Update Stock")
        products = get_all_products()
        
        if not products:
            st.info("No products to update.")
        else:
            from database import update_product, get_product_by_id
            
            product_list = {p[1]: p for p in products}
            selected_product_name = st.selectbox("Select Product to Update", list(product_list.keys()), key="select_product_update")
            selected_product = product_list[selected_product_name]
            
            product_id, name, category, buying_price, selling_price, quantity = selected_product
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                new_category = st.selectbox("Category", ["Groceries", "Dairy", "Beverages", "Household", "Other"], 
                                          index=["Groceries", "Dairy", "Beverages", "Household", "Other"].index(category), key="category_update_product")
                new_buying_price = st.number_input("Buying Price", value=buying_price, step=0.50)
            
            with col2:
                new_quantity = st.number_input("New Quantity", value=quantity, step=1)
                new_selling_price = st.number_input("Selling Price", value=selling_price, step=0.50)
            
            if st.button("🔄 Update Product", use_container_width=True):
                success, message = update_product(product_id, name, new_category, new_buying_price, new_selling_price, new_quantity)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with tab3:
        st.subheader("All Products in Inventory")
        products = get_all_products()
        
        if products:
            products_df = pd.DataFrame(products, columns=[
                'ID', 'Product', 'Category', 'Buy Price', 'Sell Price', 'In Stock'
            ])
            
            st.dataframe(
                products_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'ID': st.column_config.NumberColumn("ID", width="small"),
                    'Product': st.column_config.TextColumn("Product Name", width="medium"),
                    'Category': st.column_config.TextColumn("Category", width="small"),
                    'Buy Price': st.column_config.NumberColumn("Buy Price", format="KES %.2f", width="small"),
                    'Sell Price': st.column_config.NumberColumn("Sell Price", format="KES %.2f", width="small"),
                    'In Stock': st.column_config.NumberColumn("In Stock", width="small"),
                }
            )
            
            # Delete product section
            st.divider()
            st.subheader("Delete Product")
            product_to_delete = st.selectbox("Select product to delete", 
                                            [p[1] for p in products],
                                            key="delete_select")
            
            if st.button("❌ Delete Product", use_container_width=True):
                from database import delete_product
                product_id = next(p[0] for p in products if p[1] == product_to_delete)
                delete_product(product_id)
                st.success(f"Product '{product_to_delete}' deleted successfully")
                st.rerun()
        else:
            st.info("No products in inventory yet.")

elif page == "📋 Reports":
    st.title("📋 Sales Reports")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Daily Report", "Weekly Report", "Custom Date Range", "⚙️ System Reset"])
    
    with tab1:
        st.subheader("Today's Sales Report")
        summary = get_today_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", f"KES {summary['total_sales']:.2f}")
        with col2:
            st.metric("Total Profit", f"KES {summary['total_profit']:.2f}")
        with col3:
            st.metric("Items Sold", f"{summary['total_items_sold']}")
        with col4:
            st.metric("Transactions", f"{summary['transaction_count']}")
        
        # Profit margin
        if summary['total_sales'] > 0:
            profit_margin = (summary['total_profit'] / summary['total_sales']) * 100
            st.info(f"Profit Margin: {profit_margin:.1f}%")
    
    with tab2:
        st.subheader("Weekly Sales Report")
        from database import get_sales_by_date_range
        
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = today
        
        start_date = week_start.strftime('%Y-%m-%d')
        end_date = week_end.strftime('%Y-%m-%d')
        
        sales_data = get_sales_by_date_range(start_date, end_date)
        
        if sales_data:
            sales_df = pd.DataFrame(sales_data, columns=[
                'ID', 'Product', 'Qty', 'Price', 'Total', 'Profit', 'Payment', 'Time'
            ])
            sales_df['Date'] = pd.to_datetime(sales_df['Time']).dt.strftime('%Y-%m-%d')
            
            # Summary by date
            daily_summary = sales_df.groupby('Date').agg({
                'Total': 'sum',
                'Profit': 'sum',
                'Qty': 'sum'
            }).reset_index()
            daily_summary.columns = ['Date', 'Total Sales', 'Total Profit', 'Items Sold']
            
            st.dataframe(daily_summary, use_container_width=True, hide_index=True)
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Weekly Sales", f"KES {sales_df['Total'].sum():.2f}")
            with col2:
                st.metric("Weekly Profit", f"KES {sales_df['Profit'].sum():.2f}")
            with col3:
                st.metric("Items Sold", f"{sales_df['Qty'].sum()}")
        else:
            st.info("No sales in this week")
    
    with tab3:
        st.subheader("Custom Date Range Report")
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=7))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now())
        
        if st.button("📊 Generate Report"):
            from database import get_sales_by_date_range
            
            sales_data = get_sales_by_date_range(
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
            
            if sales_data:
                sales_df = pd.DataFrame(sales_data, columns=[
                    'ID', 'Product', 'Qty', 'Price', 'Total', 'Profit', 'Payment', 'Time'
                ])
                
                st.dataframe(sales_df, use_container_width=True, hide_index=True)
                
                st.divider()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Sales", f"KES {sales_df['Total'].sum():.2f}")
                with col2:
                    st.metric("Total Profit", f"KES {sales_df['Profit'].sum():.2f}")
                with col3:
                    st.metric("Items Sold", f"{sales_df['Qty'].sum()}")
            else:
                st.info("No sales found in this date range")
    
    with tab4:
        st.subheader("⚙️ System Reset & Maintenance")
        st.warning("⚠️ Warning: These actions will permanently delete data. This cannot be undone!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Clear Sales Only")
            st.write("Delete all sales transactions but keep products")
            if st.button("🗑️ Delete All Sales", key="clear_sales"):
                from database import clear_all_sales
                try:
                    clear_all_sales()
                    st.success("✅ All sales records deleted successfully!")
                    st.info("Products are still in inventory. You can start recording new sales.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            st.subheader("Clear Products Only")
            st.write("Delete all products but keep sales history")
            if st.button("🗑️ Delete All Products", key="clear_products"):
                from database import clear_all_products
                try:
                    clear_all_products()
                    st.success("✅ All products deleted successfully!")
                    st.info("Sales history is preserved. Add new products to continue.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.divider()
        
        st.subheader("🔄 Complete System Reset")
        st.write("**Delete everything and start completely fresh**")
        st.write("This will delete all products, sales, and reset the entire database.")
        
        if st.checkbox("I understand this will delete ALL data"):
            if st.button("🔄 Reset Entire System", type="secondary", use_container_width=True):
                from database import reset_database
                try:
                    reset_database()
                    st.success("✅ System reset successfully!")
                    st.info("The database has been reset. All tables are empty and ready for fresh data.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
