from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui

from simulation import Simulation

app_ui = ui.page_fluid(
    ui.panel_title('Memory Simulation'),  # 1
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_numeric(id="attention_level", label="Attention Level", value=0.3, min=0, max=1)
        ),
        ui.panel_main(
            ui.output_text("results"),  # 4
        )
    ))


def server(input: Inputs, output: Outputs, session: Session):
    @output(id="results")
    @render.text
    def results():
        s = Simulation()
        s.preload("./data/BRM-emot-submit.csv")
        g = ""
        for word_pairs in s.run():
            g += f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} \n"
        return g


app = App(app_ui, server)
