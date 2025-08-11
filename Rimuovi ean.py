import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="🛠️ Rimuovi codici da file Excel/CSV",
    layout="centered",
    page_icon="🛠️"
)

st.title("🛠️ Tool per rimuovere codici da file Excel/CSV")

st.sidebar.header("📋 Istruzioni")
st.sidebar.markdown("""
1. Carica il **file principale** con i dati da filtrare (Excel o CSV).  
2. Carica il **file con codici da rimuovere** (Excel o CSV).  
3. Seleziona la colonna chiave in entrambi i file (la colonna con i codici).  
4. Clicca su **Rimuovi codici** per filtrare i dati.  
5. Scarica il file filtrato pronto all’uso.

**Suggerimenti:**  
- Le colonne chiave possono avere nomi diversi, basta selezionarle correttamente.  
- Usa Excel, LibreOffice o Google Sheets per rinominare le colonne se serve.  
- Formati supportati: `.xlsx` e `.csv`.  
- [Scarica file esempio](https://github.com/tuo-repo/file-esempio.xlsx) (metti il tuo link qui)
""")

def load_file(label):
    uploaded_file = st.file_uploader(label, type=['xlsx', 'csv'])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Errore nel caricamento del file: {e}")
    return None

def remove_codes(df_main, df_remove, col_main, col_remove):
    if col_main not in df_main.columns:
        st.error(f"Colonna '{col_main}' non trovata nel file principale.")
        return None, 0, None
    if col_remove not in df_remove.columns:
        st.error(f"Colonna '{col_remove}' non trovata nel file codici da rimuovere.")
        return None, 0, None
    
    codes_to_remove = df_remove[col_remove].dropna().astype(str).str.strip().drop_duplicates().tolist()
    main_codes = df_main[col_main].astype(str).str.strip()

    mask_remove = main_codes.isin(codes_to_remove)
    filtered_df = df_main[~mask_remove]

    removed_count = mask_remove.sum()
    removed_preview = df_main[mask_remove].head(10)
    
    return filtered_df, removed_count, removed_preview

df_main = load_file("📂 Carica il file principale (Excel o CSV)")
df_remove = load_file("📂 Carica il file con i codici da rimuovere (Excel o CSV)")

if df_main is not None and df_remove is not None:
    st.subheader("Anteprima file principale")
    st.dataframe(df_main.head())

    st.subheader("Anteprima file codici da rimuovere")
    st.dataframe(df_remove.head())

    col_main = st.selectbox(
        "Seleziona la colonna chiave nel file principale",
        options=list(df_main.columns),
        format_func=lambda x: f"{x} ⓘ",
        help="Seleziona la colonna che contiene i codici da filtrare nel file principale."
    )
    col_remove = st.selectbox(
        "Seleziona la colonna chiave nel file codici da rimuovere",
        options=list(df_remove.columns),
        format_func=lambda x: f"{x} ⓘ",
        help="Seleziona la colonna che contiene i codici da rimuovere."
    )

    if st.button("🧹 Rimuovi codici"):
        filtered_df, removed_count, removed_preview = remove_codes(df_main, df_remove, col_main, col_remove)
        if filtered_df is not None:
            st.success(f"✅ Rimossi {removed_count} elementi dal file principale.")
            
            if removed_count > 0:
                st.subheader("Esempio di codici rimossi")
                st.dataframe(removed_preview)
            else:
                st.info("Nessun codice trovato da rimuovere.")

            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Filtrato')
            output.seek(0)

            st.download_button(
                label="📥 Scarica il file filtrato",
                data=output,
                file_name="file_filtrato.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
else:
    st.info("Carica entrambi i file per iniziare.")
