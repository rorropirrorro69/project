import pandas as pd
import plotly.express as px
import streamlit as st
import os

# --- Configuración de la Página ---
st.set_page_config(layout="wide")

# --- Encabezado ---
st.header("Análisis de Datos de Vehículos 🚗")
st.write("Panel de control interactivo para explorar anuncios de venta de coches.")

# --- Carga de Datos ---
try:
    csv_path = os.path.join(os.path.dirname(__file__), 'vehicles_us.csv')
    car_data = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error("Error: Archivo 'vehicles_us.csv' no encontrado. Asegúrate de que está en la carpeta principal.")
    st.stop()

# --- Creación de la Columna 'manufacturer' ---
# LÍNEA NUEVA: Extrae el fabricante de la columna 'model'
car_data['manufacturer'] = car_data['model'].apply(lambda x: str(x).split()[0])


# --- Limpieza de Datos Básica ---
if car_data['model_year'].isnull().any():
    median_model_year = car_data['model_year'].median()
    car_data['model_year'].fillna(median_model_year, inplace=True)
    car_data['model_year'] = car_data['model_year'].astype(int)

# --- Visor de Datos ---
st.subheader("Visor de Datos")
if st.checkbox("Mostrar el conjunto de datos completo"):
    st.dataframe(car_data)

# --- Gráfico de Barras: Tipos de Vehículo por Fabricante ---
st.subheader("Tipos de vehículo por fabricante")
fig_bar = px.bar(
    car_data,
    x="manufacturer",
    color="type",
    title="Cantidad de cada tipo de vehículo por fabricante"
)
fig_bar.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig_bar, use_container_width=True)

# --- Histograma: Condición vs. Año del Modelo ---
st.subheader("Histograma de Condición vs. Año del Modelo")
fig_hist_condition = px.histogram(
    car_data,
    x="model_year",
    color="condition",
    title="Distribución de la condición del vehículo por año del modelo"
)
st.plotly_chart(fig_hist_condition, use_container_width=True)

# --- Comparación de Distribución de Precios ---
st.subheader("Comparar la distribución de precios entre fabricantes")
manufacturer_list = sorted(car_data['manufacturer'].unique())
manufacturer_1 = st.selectbox('Selecciona el fabricante 1:', manufacturer_list, index=manufacturer_list.index("chevrolet") if "chevrolet" in manufacturer_list else 0)
manufacturer_2 = st.selectbox('Selecciona el fabricante 2:', manufacturer_list, index=manufacturer_list.index("bmw") if "bmw" in manufacturer_list else 1)

normalize_hist = st.checkbox("Normalizar histograma", value=True)

filtered_manufacturers = car_data[car_data['manufacturer'].isin([manufacturer_1, manufacturer_2])]

fig_price_comparison = px.histogram(
    filtered_manufacturers,
    x="price",
    color="manufacturer",
    barmode="overlay",
    histnorm='percent' if normalize_hist else None,
    title=f"Distribución de precios para {manufacturer_1} y {manufacturer_2}"
)
fig_price_comparison.update_layout(xaxis_title="Precio (USD)", yaxis_title="Porcentaje" if normalize_hist else "Cantidad")
st.plotly_chart(fig_price_comparison, use_container_width=True)