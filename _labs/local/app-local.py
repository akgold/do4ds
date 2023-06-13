from shiny import App, render, ui, reactive
import pandas as pd
from pins import board_folder
from vetiver import pin_read_write as pin
from vetiver import predict

# Load the model
model_board = board_folder("/Users/alexkgold/Documents/do4ds/_labs/local/model", allow_pickle_read = True)
model = pin.vetiver_pin_read(model_board, "penguin_model")

# App UI
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

# App Server
def server(input, output, session):
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
        return predict(model, pd.DataFrame(vals()))

    @output
    @render.text
    def vals_out():
        return f"{vals()}"

    @output
    @render.text
    def pred_out():
        return f"{round(pred())}"

app = App(app_ui, server)
