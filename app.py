import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(
    page_title="Contaminación Río Rímac",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ModeloMetalesStreamlit:
    def __init__(self):
        self.metales = {
            'Plomo': {'limite': 0.05, 'color': 'red', 'peligro': 'Daño cerebral en niños'},
            'Zinc': {'limite': 5.0, 'color': 'blue', 'peligro': 'Problemas digestivos'},
            'Cobre': {'limite': 2.0, 'color': 'orange', 'peligro': 'Problemas hepáticos'},
            'Manganeso': {'limite': 0.1, 'color': 'purple', 'peligro': 'Problemas neurológicos'}
        }

    def crear_interfaz(self):
        """Interfaz Streamlit para el modelo de contaminación"""
        
        # Título principal
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;">
            <h1>🌊 ¿Sabías que el agua de Lima viene del Río Rímac?</h1>
            <h3>Y este río recibe metales de minas en los Andes que pueden afectar tu salud</h3>
        </div>
        """, unsafe_allow_html=True)

        # Explicación del problema
        with st.expander("🔍 **EL PROBLEMA CIENTÍFICO**", expanded=True):
            st.markdown("""
            - **8 millones de personas** en Lima toman agua del Río Rímac
            - **Minas en los Andes** liberan metales pesados al río  
            - Estos metales **viajan y se acumulan** en el agua que llega a Lima
            - Esto se llama **EFECTOS ACUMULATIVOS**
            """)

        # ===== CONTROLES INTERACTIVOS =====
        st.markdown("---")
        st.header("🎮 Experimenta con el Modelo")
        st.markdown("*Cambia los controles y observa cómo afecta la contaminación*")

        col1, col2, col3 = st.columns(3)

        with col1:
            metal_seleccionado = st.selectbox(
                "🧪 **Elegir metal:**",
                options=list(self.metales.keys()),
                index=0
            )

        with col2:
            actividad_minera = st.slider(
                "🏭 **Actividad minera (%):**",
                min_value=0,
                max_value=100,
                value=60,
                help="Nivel de actividad minera en los Andes"
            )

        with col3:
            tratamiento_agua = st.slider(
                "💧 **Tratamiento de agua (%):**",
                min_value=0,
                max_value=100,
                value=30,
                help="Eficiencia del tratamiento de agua potable"
            )

        # ===== CÁLCULOS =====
        nivel_mineria = actividad_minera / 100
        nivel_tratamiento = tratamiento_agua / 100

        # Contaminación en diferentes puntos
        metal = self.metales[metal_seleccionado]
        contaminacion_minas = metal['limite'] * (0.5 + nivel_mineria * 3)
        contaminacion_lima_sin_tratamiento = contaminacion_minas * 0.7
        contaminacion_lima_con_tratamiento = contaminacion_lima_sin_tratamiento * (1 - nivel_tratamiento * 0.8)

        # ===== GRÁFICOS =====
        st.markdown("---")
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.subheader("🚚 Viaje de los Metales por el Río Rímac")
            
            # Datos para el gráfico de barras
            ubicaciones = ['Minas en los Andes', 'Mitad del Río', 'Toma de Agua Lima']
            valores_contaminacion = [
                contaminacion_minas,
                contaminacion_lima_sin_tratamiento,
                contaminacion_lima_con_tratamiento
            ]

            # Crear gráfico
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            
            # Colores según nivel de peligro
            colores = []
            for valor in valores_contaminacion:
                if valor > metal['limite']:
                    colores.append('#ff6b6b')  # Rojo - peligro
                elif valor > metal['limite'] * 0.8:
                    colores.append('#ffd93d')  # Amarillo - advertencia
                else:
                    colores.append('#6bcf7f')  # Verde - seguro

            bars = ax1.bar(ubicaciones, valores_contaminacion, color=colores, alpha=0.8, edgecolor='black')

            # Línea de límite permitido
            ax1.axhline(y=metal['limite'], color='black', linestyle='--',
                       linewidth=3, label=f'Límite seguro: {metal["limite"]} mg/L')

            # Mejorar la gráfica
            ax1.set_ylabel(f'Contaminación de {metal_seleccionado} (mg/L)', fontweight='bold')
            ax1.legend()

            # Agregar valores en las barras
            for bar, valor in zip(bars, valores_contaminacion):
                altura = bar.get_height()
                color_texto = 'white' if valor > metal['limite'] else 'black'
                ax1.text(bar.get_x() + bar.get_width()/2, altura + 0.1,
                        f'{valor:.2f}', ha='center', va='bottom',
                        fontweight='bold', color=color_texto, fontsize=12)

            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=15)
            st.pyplot(fig1)

        with col_graf2:
            st.subheader("📈 Evolución de la Contaminación 2004-2010")
            
            # Simular tendencia temporal
            años = [2004, 2005, 2006, 2007, 2008, 2009, 2010]
            tendencia = []
            for i, año in enumerate(años):
                base = contaminacion_lima_con_tratamiento * (0.8 + i * 0.05)
                tendencia.append(base)

            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.plot(años, tendencia, 'o-', linewidth=4, markersize=8,
                    color=metal['color'], label=f'Contaminación {metal_seleccionado}')
            ax2.axhline(y=metal['limite'], color='black', linestyle='--',
                       linewidth=3, label='Límite seguro')

            # Colorear áreas de peligro
            ax2.fill_between(años, tendencia, metal['limite'],
                           where=[t > metal['limite'] for t in tendencia],
                           color='red', alpha=0.2, label='Zona de Peligro')
            ax2.fill_between(años, tendencia, metal['limite'],
                           where=[t <= metal['limite'] for t in tendencia],
                           color='green', alpha=0.2, label='Zona Segura')

            ax2.set_xlabel('Año', fontweight='bold')
            ax2.set_ylabel(f'Contaminación en Lima (mg/L)', fontweight='bold')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)

        # ===== RESULTADOS Y RIESGOS =====
        st.markdown("---")
        
        # Calcular nivel de riesgo
        veces_limite = contaminacion_lima_con_tratamiento / metal['limite']

        if veces_limite > 1.5:
            nivel_riesgo = "ALTO RIESGO 🚨"
            color_riesgo = "#ff4444"
            recomendacion = "El agua presenta peligro para la salud. Se requiere acción inmediata."
        elif veces_limite > 1.0:
            nivel_riesgo = "RIESGO MODERADO ⚠️"
            color_riesgo = "#ffaa00"
            recomendacion = "El agua excede límites seguros. Se recomienda mejorar el tratamiento."
        elif veces_limite > 0.8:
            nivel_riesgo = "ALERTA BAJA 📋"
            color_riesgo = "#ffd700"
            recomendacion = "El agua está cerca del límite. Monitoreo constante necesario."
        else:
            nivel_riesgo = "SITUACIÓN SEGURA ✅"
            color_riesgo = "#44ff44"
            recomendacion = "El agua cumple con los estándares de seguridad."

        # Mostrar resultados
        st.markdown(f"""
        <div style="background: {color_riesgo}; padding: 25px; border-radius: 15px; margin: 20px 0; text-align: center; color: {'white' if veces_limite > 1.0 else 'black'};">
            <h2>{nivel_riesgo}</h2>
            <h3>El agua de Lima tiene {veces_limite:.1f} veces el límite seguro de {metal_seleccionado}</h3>
        </div>
        """, unsafe_allow_html=True)

        # ===== INFORMACIÓN DETALLADA =====
        col_info1, col_info2 = st.columns(2)

        with col_info1:
            with st.expander("🔬 **INFORMACIÓN DEL METAL**"):
                st.markdown(f"""
                **Límite seguro:** {metal['limite']} mg/L  
                **Riesgo para la salud:** {metal['peligro']}  
                **Recomendación:** {recomendacion}
                """)

        with col_info2:
            with st.expander("📚 **EFECTOS ACUMULATIVOS**"):
                st.markdown("""
                Los metales de las minas **no desaparecen** en el río. Se van **acumulando** en el camino
                y llegan hasta el agua que tomamos en Lima. Por eso, aunque las minas estén lejos en los Andes,
                **su contaminación nos afecta directamente**.

                **Más minería → Más metales en el río → Más contaminación en Lima**
                """)

        # ===== CONCLUSIÓN =====
        st.markdown("---")
        st.header("💡 ¿Qué hemos aprendido?")

        col_ap1, col_ap2 = st.columns(2)

        with col_ap1:
            st.subheader("🎯 **Puntos Clave:**")
            st.markdown("""
            1. **El agua de Lima viene del Río Rímac** 🌊
            2. **Las minas en los Andes liberan metales** que viajan por el río ⛏️
            3. **Estos metales se acumulan** y llegan hasta nuestra agua 🚰
            4. **Algunos metales pueden afectar la salud** si exceden los límites seguros 🏥
            """)

        with col_ap2:
            st.subheader("🛡️ **¿Qué podemos hacer?**")
            st.markdown("""
            - **Controlar la actividad minera** responsable
            - **Mejorar el tratamiento** de agua potable
            - **Monitorear constantemente** la calidad del agua
            - **Exigir prácticas mineras** más seguras
            """)

        st.info("""
        **🔬 Base Científica:** Este modelo se basa en el estudio *"Modeling cumulative effects of heavy metal contamination 
        in mining areas of the Rimac basin"* que analizó datos reales de 2004-2010.
        """)

# Ejecutar la aplicación
if __name__ == "__main__":
    modelo = ModeloMetalesStreamlit()
    modelo.crear_interfaz()