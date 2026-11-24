import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

st.set_page_config(page_title="Inventario TechZone", layout="wide")
st.title("Sistema de Gestión y Análisis de Inventario - TechZone S.R.L.")

ARCHIVO = "InventarioTechZone.xlsx"

# Pregunta 1: Carga del inventario
try:
    df = pd.read_excel(ARCHIVO)
except FileNotFoundError:
    st.error(f"No se encontró el archivo '{ARCHIVO}'. Comprueba que esté en la misma carpeta que la aplicación.")
    st.stop()
except Exception as e:
    st.error(f"No se pudo abrir el archivo: {e}")
    st.stop()


# Pregunta 2: Conversión de fecha y tabla 
df["FechaIngreso"] = pd.to_datetime(df["FechaIngreso"])

# Pregunta 10: Cálculos y métricas
COLUMNAS_BASE = ["Codigo", "Producto", "Categoria", "Precio", "Stock", "FechaIngreso", "Estado"]

df["ValorTotal"] = df["Precio"] * df["Stock"]
df["MargenGanancia"] = df["Precio"] * 0.12
df["DiasEnInventario"] = (pd.Timestamp.today().normalize() - df["FechaIngreso"]).dt.days

st.header("Inventario completo")
st.dataframe(df)


# Filtros interactivos
st.sidebar.header("Filtros del inventario")
df_filtrado = df.copy()

# Pregunta 3: Filtro por categoría (una o múltiples)
categorias = ["Laptop", "Monitor", "Accesorio", "Periférico", "Componente"]
categorias_sel = st.sidebar.multiselect(
    "Categoría del producto",
    options=categorias,
    default=categorias
)
df_filtrado = df_filtrado[df_filtrado["Categoria"].isin(categorias_sel)]

# Pregunta 4: Filtro por estado
estados = ["Todos", "Disponible", "Agotado", "Descontinuado", "Crítico"]
estado_sel = st.sidebar.selectbox("Estado del producto", estados)
if estado_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Estado"] == estado_sel]


# Pregunta 5: Filtro por rango de precios
precio_min = int(df["Precio"].min())
precio_max = int(df["Precio"].max())
rango_precio = st.sidebar.slider(
    "Rango de precios",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max)
)
df_filtrado = df_filtrado[
    (df_filtrado["Precio"] >= rango_precio[0]) &
    (df_filtrado["Precio"] <= rango_precio[1])
]    

# Pregunta 6: Búsqueda por nombre o palabra clave
busqueda = st.sidebar.text_input("Buscar producto (nombre o palabra clave)")
if busqueda:
    df_filtrado = df_filtrado[
        df_filtrado["Producto"].str.contains(busqueda, case=False, na=False)
    ]


# Pregunta 7: Filtro por stock mínimo (activado con checkbox)
activar_stock = st.sidebar.checkbox("Filtrar por stock mínimo")
if activar_stock:
    stock_minimo = st.sidebar.number_input(
        "Stock mínimo",
        min_value=0,
        max_value=int(df["Stock"].max()),
        value=10,
        step=1
    )
    df_filtrado = df_filtrado[df_filtrado["Stock"] >= stock_minimo]


# Tabla filtrada
st.header("Inventario filtrado")
st.write(f"Productos encontrados: {len(df_filtrado)}")
st.dataframe(df_filtrado)


# Pregunta 8: Registro de nuevos productos
st.header("Registro de nuevos productos")

def generar_codigo():
    # Código único con el formato del inventario: PR-AAMMDD-HHMMSS
    return "PR-" + datetime.now().strftime("%y%m%d-%H%M%S")

def determinar_estado(stock, descontinuado):
    # Pregunta 9: estado automático según el stock
    if descontinuado:
        return "Descontinuado"
    elif stock == 0:
        return "Agotado"
    elif stock < 5:
        return "Crítico"
    else:
        return "Disponible"
    
with st.form("form_registro", clear_on_submit=True):
    nombre = st.text_input("Nombre del producto")
    categoria = st.selectbox("Categoría", categorias)
    precio = st.number_input("Precio unitario", min_value=0.0, step=1.0)
    stock = st.number_input("Stock disponible", min_value=0, step=1)
    fecha_ingreso = st.date_input("Fecha de ingreso", value=date.today())
    descontinuado = st.checkbox("Marcar como descontinuado")
    enviar = st.form_submit_button("Registrar producto")

if enviar:
    errores = []
    if nombre.strip() == "":
        errores.append("El nombre del producto no puede estar vacío.")
    if precio <= 0:
        errores.append("El precio debe ser mayor que 0.")
    if stock < 0:
        errores.append("El stock debe ser mayor o igual a 0.")
    if fecha_ingreso > date.today():
        errores.append("La fecha de ingreso no puede ser futura.")

    if errores:
        for error in errores:
            st.error(error)
    else:
        nuevo = pd.DataFrame([{
            "Codigo": generar_codigo(),
            "Producto": nombre.strip(),
            "Categoria": categoria,
            "Precio": precio,
            "Stock": int(stock),
            "FechaIngreso": pd.to_datetime(fecha_ingreso),
            "Estado": determinar_estado(stock, descontinuado)
        }])
        df_actualizado = pd.concat([df[COLUMNAS_BASE], nuevo], ignore_index=True)
        try:
            df_actualizado.to_excel(ARCHIVO, index=False)
            st.success(f"Producto '{nombre}' registrado con el código {nuevo['Codigo'][0]}. "
                       f"Pulsa R para verlo en el inventario.")
        except PermissionError:
            st.error("No se pudo guardar: cierra el archivo Excel si lo tienes abierto.")


# Pregunta 11: Gráficos
st.header("Gráficos del inventario")

productos_por_categoria = df["Categoria"].value_counts()
valor_por_categoria = df.groupby("Categoria")["ValorTotal"].sum()

# Barras y circular uno al lado del otro en un mismo figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.bar(productos_por_categoria.index, productos_por_categoria.values)
ax1.set_title("Cantidad de productos por categoría")
ax1.set_xlabel("Categoría")
ax1.set_ylabel("Cantidad de productos")
ax1.tick_params(axis="x", rotation=45)

ax2.pie(valor_por_categoria.values, labels=valor_por_categoria.index, autopct="%1.1f%%")
ax2.set_title("Valor total por categoría")

plt.tight_layout()
st.pyplot(fig)

# Top 5 de productos más valiosos según ValorTotal
st.subheader("Top 5 productos más valiosos")

top5 = df.sort_values("ValorTotal", ascending=False).head(5)
etiquetas = top5["Producto"] + " (" + top5["Codigo"] + ")"

fig_top, ax_top = plt.subplots(figsize=(10, 5))
ax_top.barh(etiquetas, top5["ValorTotal"])
ax_top.invert_yaxis()
ax_top.set_title("Top 5 productos por Valor Total")
ax_top.set_xlabel("Valor Total")
plt.tight_layout()
st.pyplot(fig_top)

# He ido aniadiendo codigo segun he ido avanzando en el examen, 
# por eso puedes ver alguan pregunta respondida en alguna parte del codigo