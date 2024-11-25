import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import plotly.figure_factory as ff


# Judul aplikasi
st.title("Dashboard Data Visualisai Anak Soleh")

# Menampilkan data
data = pd.read_csv('New-amazon-cleaning.csv')

# Menghapus kolom 'Unnamed: 0' jika ada
if 'Unnamed: 0' in data.columns:
    data = data.drop(columns=['Unnamed: 0'])

# header
st.header("Distribusi Rating Produk")

# Menghitung jumlah setiap rating
rating_counts = data['rating'].value_counts().sort_index()

# Membuat figure gabungan
fig = go.Figure()

# Menambahkan bar chart
fig.add_trace(go.Bar(
    x=rating_counts.index,  # Nilai rating
    y=rating_counts.values,  # Frekuensi rating
    name="Bar Chart",
    marker=dict(color='skyblue'),
    opacity=0.6
))

# Menambahkan line chart
fig.add_trace(go.Scatter(
    x=rating_counts.index,  # Nilai rating
    y=rating_counts.values,  # Frekuensi rating
    name="Line Chart",
    mode='lines+markers',
    line=dict(color='blue', width=2),
    marker=dict(size=8)
))

# Menambahkan layout
fig.update_layout(
    xaxis_title="Rating",
    yaxis_title="Produk",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_white"
)

# Menampilkan grafik di Streamlit
st.plotly_chart(fig)



# Header untuk visualisasi hubungan
st.header("Hubungan Antara Actual Price, Discount Price, dan Rating")

# Mengelompokkan data berdasarkan rating untuk mendapatkan harga rata-rata
grouped_data = data.groupby('rating').agg(
    actual_price_mean=('actual_price', 'mean'),
    discounted_price_mean=('discounted_price', 'mean')
).reset_index()

# Membuat bar chart dengan Plotly
fig = go.Figure()

# Menambahkan bar chart untuk actual_price
fig.add_trace(go.Bar(
    x=grouped_data['rating'],
    y=grouped_data['actual_price_mean'],
    name='Harga Asli',
    marker=dict(color='royalblue'),
    opacity=0.6
))

# Menambahkan bar chart untuk discounted_price
fig.add_trace(go.Bar(
    x=grouped_data['rating'],
    y=grouped_data['discounted_price_mean'],
    name='Harga Setelah Diskon',
    marker=dict(color='orange'),
    opacity=0.6
))

# Menambahkan layout dan pengaturan visual
fig.update_layout(
    xaxis_title="Rating Produk",
    yaxis_title="Harga Rata-rata",
    barmode='group',  # Mengelompokkan batang berdasarkan rating
    template="plotly_white",
    legend_title="Jenis Harga"
)

# Menampilkan bar chart interaktif di Streamlit
st.plotly_chart(fig)


# Header untuk visualisasi Correlation Matrix untuk Semua Kolom Numerik
st.header("Correlation Matrix untuk Semua Kolom Numerik")

# Memastikan ada kolom numerik dalam dataset
numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns

if len(numeric_cols) > 0:
    # Menghitung matriks korelasi
    correlation_matrix = data[numeric_cols].corr()

    # Membuat heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)
else:
    st.error("Tidak ada kolom numerik ditemukan dalam dataset.")


# Header untuk visualisasi 5 Kategori Teratas Berdasarkan Rating Produk
st.header("5 Kategori Teratas Berdasarkan Rating Produk")

# Menghitung rata-rata rating per kategori
# Gantilah 'category' dengan nama kolom kategori yang sesuai di dataset Anda
category_rating = data.groupby('category')['rating'].mean().reset_index()

# Membatasi angka rating ke dua angka di belakang koma
category_rating['rating'] = category_rating['rating'].round(2)

# Mengurutkan kategori berdasarkan rating tertinggi
top_5_categories = category_rating.sort_values(by='rating', ascending=False).head(5)

# Membuat bar chart interaktif untuk 5 kategori teratas
fig = px.bar(
    top_5_categories,
    x='category',  # Kolom kategori di sumbu-X
    y='rating',  # Rata-rata rating di sumbu-Y
    labels={'category': 'Kategori Produk', 'rating': 'Rata-rata Rating'},
    color='rating',  # Warna batang berdasarkan rating
    color_continuous_scale='Viridis',  # Skala warna
)

# Menampilkan bar chart interaktif di Streamlit
st.plotly_chart(fig)


# Header untuk visualisasi Jumlah Barang Dari Masing-Masing Category
st.header("Jumlah Barang Dari Masing-Masing Category")

# Menghitung jumlah produk per kategori
# Gantilah 'category' dengan nama kolom kategori yang sesuai di dataset Anda
category_count = data['category'].value_counts().reset_index()

# Menamai ulang kolom untuk kemudahan
category_count.columns = ['category', 'count']

# Membuat bar chart interaktif untuk jumlah produk per kategori
fig = px.bar(
    category_count,
    x='category',  # Kolom kategori di sumbu-X
    y='count',  # Jumlah produk di sumbu-Y
    labels={'category': 'Kategori Produk', 'count': 'Jumlah Produk'},
    color='count',  # Warna batang berdasarkan jumlah produk
    color_continuous_scale='Viridis',  # Skala warna
)

# Menampilkan bar chart interaktif di Streamlit
st.plotly_chart(fig)


# Header untuk visualisasi Top 5 Kategori Termurah Berdasarkan Harga Setelah Diskon
st.header("Top 5 Kategori Termurah Berdasarkan Harga Setelah Diskon")

# Menghitung rata-rata harga diskon per kategori
category_discounted_price = data.groupby('category')['discounted_price'].mean().reset_index()

# Membulatkan harga diskon menjadi angka bulat
category_discounted_price['discounted_price'] = category_discounted_price['discounted_price'].round()

# Mengurutkan berdasarkan harga diskon terendah
top_5_cheapest_categories = category_discounted_price.sort_values(by='discounted_price').head(5)

# Membuat bar chart interaktif untuk 5 kategori termurah
fig = px.bar(
    top_5_cheapest_categories,
    x='category',  # Kolom kategori di sumbu-X
    y='discounted_price',  # Rata-rata harga diskon di sumbu-Y
    labels={'category': 'Kategori Produk', 'discounted_price': 'Harga Setelah Diskon (Ribu)'},
    color='discounted_price',  # Warna batang berdasarkan harga diskon
    color_continuous_scale='YlGnBu',  # Skala warna
    text='discounted_price'  # Menampilkan harga diskon pada setiap batang
)

# Menampilkan bar chart interaktif di Streamlit
st.plotly_chart(fig)

