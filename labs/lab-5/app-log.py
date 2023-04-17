from shiny import App, render, ui, reactive
import requests
import logging

api_url = 'http://127.0.0.1:8080/predict'
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

app_ui = ui.page_fluid(
    ui.panel_title("Penguin Mass Predictor"), 
    ui.layout_sidebar(
        ui.panel_sidebar(
            [ui.input_slider("bill_length", "Bill Length (mm)", 30, 60, 45, step = 0.1),
            ui.input_select("sex", "Sex", ["Male", "Female"]),
            ui.input_select("species", "Species", ["Adelie", "Chinstrap", "Gentoo"]),
            ui.input_action_button("predict", "Predict")]
        ),
        ui.panel_main(
            ui.h2("Penguin Parameters"),
            ui.output_text_verbatim("vals_out"),
            ui.h2("Predicted Penguin Mass (g)"), 
            ui.output_text("pred_out")
        )
    )   
)

def server(input, output, session):
    logging.info("App start")

    @reactive.Calc
    def vals():
        d = {
            "bill_length_mm" : input.bill_length(),
            "sex_Male" : input.sex() == "Male",
            "species_Gentoo" : input.species() == "Gentoo", 
            "species_Chinstrap" : input.species() == "Chinstrap"

        }
        return d
    
    @reactive.Calc
    @reactive.event(input.predict)
    def pred():
        logging.info("Request Made")
        r = requests.post(api_url, json = vals())
        logging.info("Request Returned")

        if r.status_code != 200:
            logging.error("HTTP error returned")

        return r.json().get('predict')[0]

    @output
    @render.text
    def vals_out():
        return f"{vals()}"

    @output
    @render.text
    def pred_out():
        return f"{round(pred())}"

app = App(app_ui, server)
