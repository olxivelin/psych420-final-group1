from pathlib import Path

from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui

import html

# stm_markdown_file = Path(__file__).parent / "report/short_term_memory.md"
# with open(stm_markdown_file) as f:
#     stm_markdown = f.read()

report_path = Path(__file__).parent / "report"
markdown_files = report_path.glob('*.md')


def get_markdown():
    controls = []
    for filename in markdown_files:
        with open(filename) as f:
            controls.append(ui.markdown(f.read()))

    return controls

from simulation import Simulation

app_ui = ui.page_fluid(
    ui.panel_title('Memory Simulation'),  # 1
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_numeric(id="attention_level", label="Attention Level", value=0.3, min=0, max=1)
        ),
        ui.panel_main(
            ui.output_ui("results"),  # 4
            # ui.output_table(id="results"),
            ui.output_ui(id="images"),
            # ui.markdown(stm_markdown),
            get_markdown()
        )
    ))


def server(input: Inputs, output: Outputs, session: Session):
    @output(id="results")
    @render.text
    def results():
        s = Simulation()
        infile = Path(__file__).parent / "data/BRM-emot-submit.csv"
        s.preload(infile)
        g = ""
        for word_pairs in s.run():
            g += f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} <br>"
        return g

    @output
    @render.ui
    def images() -> ui.Tag:
        img = ui.img(src="Information_Processing_Model_-_Atkinson_&_Shiffrin.jpg", style="width: 400px;")
        return img


static_dir = Path(__file__).parent / "report/images"
app = App(app_ui, server, static_assets=static_dir)
