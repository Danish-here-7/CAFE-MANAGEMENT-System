
import streamlit as st
import mysql.connector
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="system",
        database="danishdb"
    )

conn = connect_db()
cursor = conn.cursor()
st.set_page_config(page_title="Café Management System", layout="wide")

# Custom CSS
st.markdown("""
    <style>

    .stApp {
            background: linear-gradient(to right, #2ce8d8, #feb47b);
     }
    h2, .stHeader {
            color:#81cf34 ; text-align: center; font-weight:800;
            }
    .stButton>button {
            background-color: #ff6600; color: white; border-radius: 100px; padding: 10px 20px;
            }
    .stButton>button:hover {
            background-color: #28b7d4;
            }
    .stTextInput input {
            border: 2px solid #ff6600; border-radius: 5px; padding: 10px;
            }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>☕ Welcome to Café Management System</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 14px; font-style: italic;'>by Danish Khajuria</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Login as Customer"): st.session_state["user_type"] = "Customer"
with col2:
    if st.button("Login as Staff"): st.session_state["user_type"] = "Staff"
with col3:
    if st.button("Login as Manager"): st.session_state["user_type"] = "Manager"

st.write(f"Current User Type: {st.session_state.get('user_type', 'Not Set')}")

# Customer Section
if st.session_state.get("user_type") == "Customer":
    st.header("🛒 Customer Section")
    st.subheader("📋 Menu")

    cursor.execute("SELECT item_name, price, image_url FROM Menu")
    menu_items = cursor.fetchall()

    order_quantities = {}

    if menu_items:
        cols = st.columns(len(menu_items))
        for i, item in enumerate(menu_items):
            with cols[i]:
                st.image(item[2], width=120)
                st.write(f"🍽 **{item[0]}** - ₹{item[1]}")
                qty = st.number_input(f"Qty - {item[0]}", min_value=0, key=item[0])
                order_quantities[item[0]] = (qty, item[1])

    customer_name = st.text_input("Enter Your Name")

    if st.button("Place Order"):
        ordered_items = [f"{name} x{qty}" for name, (qty, _) in order_quantities.items() if qty > 0]
        total_price = sum(qty * price for name, (qty, price) in order_quantities.items() if qty > 0)

        if ordered_items:
            cursor.execute("INSERT INTO Orders (customer_name, items, total_price, order_status) VALUES (%s, %s, %s, 'In Progress')",
                           (customer_name, ", ".join(ordered_items), total_price))
            conn.commit()
            st.success(f"✅ Order placed! Bill: ₹{total_price}")

# Staff Section
elif st.session_state.get("user_type") == "Staff":
    st.header("👨‍🍳 Staff Section")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM Staffs WHERE username = %s AND password = %s", (username, password))
        staff = cursor.fetchone()
        if staff:
            st.session_state["logged_in"] = True
            st.session_state["staff_role"] = staff[2]
            st.success(f"✅ Login Successful as {staff[2]}")

    if st.session_state.get("logged_in"):
        st.subheader("📋 Orders to Prepare")
        cursor.execute("SELECT id, customer_name, items, total_price, order_status FROM Orders WHERE order_status = 'In Progress'")

        for order in cursor.fetchall():
            st.write(f"🆔 Order ID: {order[0]}, Customer: {order[1]}, Items: {order[2]}, Total: ₹{order[3]}, Status: {order[4]}")
            if st.button(f"Mark Order {order[0]} as Ready", key=f"ready_{order[0]}"):
                cursor.execute("UPDATE Orders SET order_status = 'Completed' WHERE id = %s", (order[0],))
                conn.commit()
                st.success(f"✅ Order {order[0]} marked as Ready!")

        st.subheader("📦 All Orders")
        cursor.execute("SELECT id, customer_name, items, total_price, order_status FROM Orders")
        all_orders = cursor.fetchall()

        for order in all_orders:
            st.write(f"🧾 Order ID: {order[0]}, Customer: {order[1]}, Items: {order[2]}, Total: ₹{order[3]}, Status: {order[4]}")

# Manager Section
elif st.session_state.get("user_type") == "Manager":
    st.header("👨‍💼 Manager Section")
    manager_name = st.text_input("Manager Name")
    manager_password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM Manager WHERE name = %s AND password = %s", (manager_name, manager_password))
        manager = cursor.fetchone()
        if manager:
            st.session_state["logged_in"] = True
            st.success("✅ Login Successful")

    if st.session_state.get("logged_in"):
        st.subheader("📜 Manage Menu")
        action = st.radio("Choose Action", ["Add Item", "Remove Item", "Update Price"])

        if action == "Add Item":
            name = st.text_input("Item Name")
            price = st.number_input("Price", min_value=0.0)
            image_url = st.text_input("Image URL")

            if st.button("Add"):
                cursor.execute("INSERT INTO Menu (item_name, price, image_url) VALUES (%s, %s, %s)", (name, price, image_url))
                conn.commit()
                st.success(f"✅ {name} added!")

        elif action == "Remove Item":
            cursor.execute("SELECT item_name FROM Menu")
            items = [item[0] for item in cursor.fetchall()]
            remove_item = st.selectbox("Select Item", items)

            if st.button("Remove"):
                cursor.execute("DELETE FROM Menu WHERE item_name = %s", (remove_item,))
                conn.commit()
                st.success(f"✅ {remove_item} removed!")

        elif action == "Update Price":
            cursor.execute("SELECT item_name FROM Menu")
            items = [item[0] for item in cursor.fetchall()]
            update_item = st.selectbox("Select Item", items)
            new_price = st.number_input("New Price", min_value=0.0)

            if st.button("Update"):
                cursor.execute("UPDATE Menu SET price = %s WHERE item_name = %s", (new_price, update_item))
                conn.commit()
                st.success(f"✅ Price updated!")
conn.close()
