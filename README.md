# Sistema de Gestión y Análisis de Inventario - TechZone S.R.L.

Aplicación web desarrollada con **Streamlit** para gestionar y analizar el inventario de productos tecnológicos de la empresa TechZone S.R.L. Los datos se leen y se guardan en un archivo Excel (`InventarioTechZone.xlsx`).

Proyecto realizado para el examen práctico del Tema 2 del Módulo 11 "Aplicaciones Interactivas para Análisis de Datos e Inteligencia Artificial" del Executive Master en IA (INTECSSA).

## Funcionalidades

- **Inventario completo** con columnas calculadas: Valor Total, Margen de Ganancia (12 %) y Días en Inventario.
- **Filtros interactivos** en la barra lateral:
  - Categoría (selección múltiple)
  - Estado del producto
  - Rango de precios
  - Búsqueda por nombre o palabra clave
  - Stock mínimo (se activa con una casilla)
- **Registro de nuevos productos** mediante formulario, con:
  - Código único generado automáticamente (`PR-AAMMDD-HHMMSS`)
  - Estado asignado según el stock (Disponible, Crítico, Agotado o Descontinuado)
  - Validación de los datos introducidos
- **Gráficos** con Matplotlib:
  - Cantidad de productos por categoría
  - Valor total por categoría
  - Top 5 productos más valiosos

## Tecnologías

- Python
- Streamlit
- Pandas
- Matplotlib
- OpenPyXL

## Estructura del proyecto

```
ExamenPracticoT2Detalles/
├── inventario_app.py         # Aplicación principal
├── InventarioTechZone.xlsx   # Datos del inventario
├── requirements.txt          # Dependencias
└── README.md
```

## Ejecución en local

1. Clonar el repositorio:
   ```
   git clone <url-del-repositorio>
   ```
2. Crear y activar un entorno virtual:
   ```
   python -m venv StreamlitVenv
   .\StreamlitVenv\Scripts\Activate.ps1
   ```
3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:
   ```
   streamlit run inventario_app.py
   ```

## Autora

Vinolia Barreto