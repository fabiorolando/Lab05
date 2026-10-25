import flet as ft
from flet.core.textfield import TextField

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    input_tipo = ft.TextField(label = "Tipo")
    input_marca = ft.TextField(label = "Marca")
    input_anno = ft.TextField(label = "Anno acquisto")
    input_cont = ft.TextField(value = '0',
                              width = 80,
                              text_align = ft.TextAlign.CENTER,
                              read_only = True)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    def incrementa_cont(e):
        valore = int(input_cont.value)    #vado a prendere il valore del TextField, ovvero zero assegnato da me prima
                                          #e lo trasformo in intero perchè era un valore stringa
        valore = valore + 1               #Incremento di uno il valore
        input_cont.value = str(valore)    #Ritrasformo in valore string
        page.update()                     #update

    def decrementa_cont(e):
        valore = int(input_cont.value)
        if valore > 0:
            valore = valore - 1
            input_cont.value = str(valore)
            page.update()

    def aggiungi_strumento(e):
        try:
            tipo = input_tipo.value.strip()
            marca = input_marca.value.strip()
            anno = int(input_anno.value)
            conteggio = float(input_cont.value)
        except ValueError:
            alert.show_alert("❌Errore: inserisci valori numerici validi per anno e costo")
            return
        deposito.aggiungi_strumento(tipo, marca, anno, conteggio)
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        input_cont.value = 0
        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    pulsante_incrementa = ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN, on_click=incrementa_cont)
    pulsante_decrementa = ft.IconButton(icon=ft.Icons.REMOVE, icon_color=ft.Colors.RED, on_click=decrementa_cont)
    pulsante_aggiungi_strumento = ft.ElevatedButton("Aggiungi strumento", on_click=aggiungi_strumento)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(spacing=10,
               controls=[input_tipo, input_marca, input_anno,pulsante_decrementa,input_cont, pulsante_incrementa],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),


        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
