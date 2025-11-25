import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

# Create a folder for uploaded images if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Database setup
conn = sqlite3.connect('lost_and_found.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS lost_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type TEXT,
    description TEXT,
    contact TEXT,
    image_path TEXT,
    date TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS found_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type TEXT,
    description TEXT,
    contact TEXT,
    image_path TEXT,
    date TEXT
)''')

conn.commit()

# Function to add lost item
def add_lost_item(item_type, description, contact, image_path):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO lost_items (item_type, description, contact, image_path, date) VALUES (?, ?, ?, ?, ?)',
              (item_type, description, contact, image_path, date))
    conn.commit()

# Function to add found item
def add_found_item(item_type, description, contact, image_path):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO found_items (item_type, description, contact, image_path, date) VALUES (?, ?, ?, ?, ?)',
              (item_type, description, contact, image_path, date))
    conn.commit()

# Function to get lost items (public view, no contact)
def get_lost_items():
    c.execute('SELECT id, item_type, description, image_path, date FROM lost_items')
    return c.fetchall()

# Function to get found items (public view, no contact)
def get_found_items():
    c.execute('SELECT id, item_type, description, image_path, date FROM found_items')
    return c.fetchall()

# Function to get all lost items with contact (for admin)
def get_lost_items_admin():
    c.execute('SELECT * FROM lost_items')
    return c.fetchall()

# Function to get all found items with contact (for admin)
def get_found_items_admin():
    c.execute('SELECT * FROM found_items')
    return c.fetchall()

# Inject custom CSS to change background and sidebar colors
st.markdown("""
    <style>
     /* Change main background to white */
    .main .block-container {
        background-color: white;
    }
    /* Change sidebar background to light blue */
    .sidebar .sidebar-content {
        background-color: lightblue;
    }
    </style>
    """,
    unsafe_allow_html=True)

# Streamlit app
st.set_page_config(page_title="Lost and Found", layout="wide")

# Header with logo on the left
col1, col2 = st.columns([1, 4])
with col1:
    st.image("Untitled-design-61.jpg", width=250)  # Replace with your custom logo path
with col2:
    st.title("Lost and Found")

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", ["Beranda", "Laporkan Barang Hilang", "Laporkan Barang Ditemukan", "Admin"])

if menu == "Beranda":
    st.header("Selamat Datang di UT Lost & Found")
    st.markdown(
        """
        <div style="text-align: center;">
    Website ini dibuat untuk membantu seluruh civitas akademika Universitas Terbuka dalam mencari atau melaporkan barang hilang di lingkungan kampus. Dengan sistem ini, mahasiswa, dosen, dan staf dapat saling membantu menemukan kembali barang-barang yang tercecer. Kami berkomitmen untuk menghadirkan platform yang aman, transparan, dan mudah digunakan agar setiap laporan dapat ditangani secara cepat dan efisien.

    **Visi & Misi**  
    **Visi**  
    Menjadi platform digital terpercaya yang memfasilitasi pelaporan dan pencarian barang hilang di lingkungan Universitas Terbuka dengan semangat kolaboratif dan tanggung jawab sosial.

    **Misi**  
    Membangun sistem pelaporan barang hilang dan ditemukan yang mudah diakses oleh seluruh warga kampus.  
    Meningkatkan kesadaran akan pentingnya kejujuran dan kepedulian sosial di lingkungan akademik.  
    Menjaga kepercayaan dengan memastikan setiap laporan diverifikasi secara transparan.

    **Tentang Kami**  
    UT Lost & Found adalah inisiatif mahasiswa Universitas Terbuka yang bekerja sama dengan unit kemahasiswaan dan layanan TI. Website ini dirancang sebagai wadah kolaboratif untuk melaporkan, mencari, dan mengembalikan barang yang hilang atau ditemukan. Kami percaya bahwa kejujuran dan kepedulian adalah nilai utama dalam menciptakan lingkungan kampus yang aman dan nyaman.

    **Hubungi Kami**  
    Jika Anda memiliki pertanyaan, saran, atau laporan khusus, silakan hubungi tim kami melalui contact center di bawah ini.

    Email: lostfound@ecampus.ut.ac.id  
    Telepon: (021) 1234-5678  
    Alamat: Jl. Cabe Raya, Pondok Cabe, Tangerang Selatan
    </div>
        """,
        unsafe_allow_html=True
    )

elif menu == "Laporkan Barang Hilang":
    st.header("Laporkan Barang Hilang")
    item_type = st.selectbox("Jenis Barang", ["Dompet", "Helmet", "Kunci", "Barang Lain"])
    description = st.text_area("Deskripsi")
    contact = st.text_input("ID atau Nomor Telepon (hanya untuk verifikasi admin)")
    uploaded_file = st.file_uploader("Lampirkan Gambar Barang", type=["jpg", "png", "jpeg"])
    if st.button("Kirim"):
        if description and contact:
            image_path = None
            if uploaded_file is not None:
                image_path = f"uploads/lost_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            add_lost_item(item_type, description, contact, image_path)
            st.success("Barang hilang berhasil dilaporkan!")
        else:
            st.error("Harap isi semua kolom.")

elif menu == "Laporkan Barang Ditemukan":
    st.header("Laporkan Barang Ditemukan")
    item_type = st.selectbox("Jenis Barang", ["Dompet", "Helmet", "Kunci", "Barang Lain"])
    description = st.text_area("Deskripsi")
    contact = st.text_input("ID atau Nomor Telepon (hanya untuk verifikasi admin)")
    uploaded_file = st.file_uploader("Lampirkan Gambar Barang", type=["jpg", "png", "jpeg"])
    if st.button("Kirim"):
        if description and contact:
            image_path = None
            if uploaded_file is not None:
                image_path = f"uploads/found_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            add_found_item(item_type, description, contact, image_path)
            st.success("Barang ditemukan berhasil dilaporkan!")
        else:
            st.error("Harap isi semua kolom.")

elif menu == "Admin":
    st.header("Panel Admin")
    password = st.text_input("Masukkan Kata Sandi Admin", type="password")
    if password == "admin123":  # Simple password, change as needed
        st.success("Akses diberikan.")
        
        st.subheader("Barang Hilang")
        lost_data = get_lost_items_admin()
        if lost_data:
            df_lost = pd.DataFrame(lost_data, columns=["ID", "Jenis Barang", "Deskripsi", "Kontak", "Path Gambar", "Tanggal"])
            st.dataframe(df_lost)
            for row in lost_data:
                if row[4]:  # If image path exists
                    st.image(row[4], caption=f"Barang Hilang ID {row[0]}")
        else:
            st.write("Tidak ada barang hilang yang dilaporkan.")
        
        st.subheader("Barang Ditemukan")
        found_data = get_found_items_admin()
        if found_data:
            df_found = pd.DataFrame(found_data, columns=["ID", "Jenis Barang", "Deskripsi", "Kontak", "Path Gambar", "Tanggal"])
            st.dataframe(df_found)
            for row in found_data:
                if row[4]:  # If image path exists
                    st.image(row[4], caption=f"Barang Ditemukan ID {row[0]}")
        else:
            st.write("Tidak ada barang ditemukan yang dilaporkan.")
        
        # Optional: Simple matching (admin can manually check)
        st.subheader("Potensi Pencocokkan")
        if lost_data and found_data:
            for lost in lost_data:
                for found in found_data:
                    if lost[1] == found[1] and lost[2].lower() in found[2].lower():  # Same type and description match
                        st.write(f"Potensi cocok: Hilang {lost[1]} - {lost[2]} dengan Ditemukan {found[1]} - {found[2]}")
                        st.write(f"Kontak Hilang: {lost[3]}, Kontak Ditemukan: {found[3]}")
        else:
            st.write("Tidak ada pencocokkan ditemukan.")
    else:
        st.error("Kata sandi salah.")

# Close database connection at the end
conn.close()
