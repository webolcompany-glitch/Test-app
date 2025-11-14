import streamlit as st
import pandas as pd

st.title("Calcolo Prezzo di Vendita con Margine Reale")

# INPUT
costo_prodotto = st.number_input("Costo prodotto (€):", min_value=0.0, value=100.0, step=0.01)
costo_spedizione = st.number_input("Costo spedizione (€):", min_value=0.0, value=13.41, step=0.01)
commissione = st.number_input("Commissione marketplace (%):", min_value=0.0, max_value=100.0, value=14.0, step=0.1)/100
iva = st.number_input("IVA (%):", min_value=0.0, max_value=100.0, value=22.0, step=0.1)/100

margine_tipo = st.selectbox("Tipo di margine desiderato:", ["Euro", "Percentuale (%)"])

if margine_tipo == "Euro":
    margine_input = st.number_input("Margine netto desiderato (€):", min_value=0.0, value=27.66, step=0.01)
elif margine_tipo == "Percentuale (%)":
    margine_input = st.number_input("Margine netto desiderato (% sul prezzo imponibile):", min_value=0.0, max_value=100.0, value=15.0, step=0.1)/100

if st.button("Calcola Prezzo Finale"):
    costo_totale = costo_prodotto + costo_spedizione

    # se margine in percentuale, trasformo in netto in euro
    if margine_tipo == "Percentuale (%)":
        netto_desiderato = margine_input  # in % del prezzo imponibile, calcoliamo P_lordo iterativamente
        # formula diretta: P_lordo = (Costo_totale / (1 - commissione - margine_percent_imponibile)) * (1 + IVA)
        P_lordo = (costo_totale / (1 - commissione - netto_desiderato)) * (1 + iva)
    else:
        # margine in euro
        denominatore = (1 / (1 + iva)) - commissione
        if denominatore <= 0:
            st.error("Errore: combinazione di commissione e IVA troppo alta, margine impossibile.")
        else:
            P_lordo = (margine_input + costo_totale) / denominatore

    # calcoli dettagliati
    imponibile = P_lordo / (1 + iva)
    iva_da_versare = P_lordo - imponibile
    commissioni_marketplace = P_lordo * commissione
    netto_reale = imponibile - costo_totale - commissioni_marketplace

    # OUTPUT
    st.subheader("Risultato")
    st.write(f"**Prezzo finale da impostare (IVA inclusa):** €{P_lordo:.2f}")
    st.write(f"**Prezzo imponibile:** €{imponibile:.2f}")
    st.write(f"**IVA da versare:** €{iva_da_versare:.2f}")
    st.write(f"**Commissioni marketplace:** €{commissioni_marketplace:.2f}")
    st.write(f"**Netto reale che rimane in tasca:** €{netto_reale:.2f}")

    # Tabella riepilogativa
    df = pd.DataFrame({
        "Voce": ["Prezzo finale lordo", "Prezzo imponibile", "IVA da versare", "Commissioni marketplace", "Netto reale"],
        "Valore (€)": [P_lordo, imponibile, iva_da_versare, commissioni_marketplace, netto_reale]
    })
    st.table(df)
