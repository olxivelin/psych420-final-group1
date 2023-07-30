from pathlib import Path

from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui

from simulation import Simulation

report_path = Path(__file__).parent / "report"


def get_all_markdown():
    controls = []
    markdown_files = report_path.glob('*.md')
    for filename in markdown_files:
        with open(filename) as f:
            controls.append(ui.markdown(f.read()))

    return controls


def get_markdown(section):
    filename = report_path / f"{section}.md"
    with open(filename) as f:
        return ui.markdown(f.read())


app_ui = ui.page_fluid(
    ui.panel_title('Memory Simulation'),  # 1
    ui.layout_sidebar(
        ui.panel_sidebar(

        ),
        ui.panel_main(
            get_markdown("background"),
            # ui.output_table(id="results"),
            get_markdown("atkinson_shiffrin_model"),
            ui.output_ui(id="images"),
            get_markdown("sensory_memory"),
            get_markdown("short_term_memory"),
            get_markdown("long_term_memory"),
            get_markdown("learning"),
            get_markdown("our_model"),
            get_markdown("simulation_1"),

            ui.input_slider(id="distraction_level", label="Distraction Level", value=20, min=0, max=100),
            ui.br(),
            ui.input_action_button("run_simulation_1", "Run Simulation"),
            ui.br(),
            ui.output_ui("simulation_1_results"),  # 4

            get_markdown("references"),


        )
    ))


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def run_simulation_1():
        input.run_simulation_1()

        distraction_level = (input.distraction_level() / 100)

        p = ui.Progress()
        p.set(1 / 30, message="Simulating, please wait...")
        s = Simulation()
        infile = Path(__file__).parent / "data/BRM-emot-submit.csv"
        p.set(5 / 30, message="Loading sensory encodings, please wait...")
        s.preload(infile)
        p.set(20 / 30, message="Simulating rehearsal over time, please wait...")
        g = ""
        for word_pairs in s.run_1(distraction_level):
            p.set(30 / 30, message="Recalling from short term memory, please wait...")
            g += f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} <br>"
        p.close()
        return g

    @output
    @render.text
    def simulation_1_results():
        return run_simulation_1()

    @output
    @render.ui
    def images() -> ui.Tag:
        img = ui.img(src="Information_Processing_Model_-_Atkinson_&_Shiffrin.jpg", style="width: 400px;")
        return img


static_dir = Path(__file__).parent / "report/images"
app = App(app_ui, server, static_assets=static_dir)
