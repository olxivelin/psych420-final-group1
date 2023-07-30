from pathlib import Path

from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui

import matplotlib.pyplot as plt
import numpy as np

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
            ui.input_numeric(id="total_time", label="Simulation Time Length (s)", value=100, min=0, max=10000),
            ui.input_text(id="word_list", label="Words to Rehearse", value="person, man, woman, camera, tv"),


            ui.br(),
            ui.input_action_button("run_simulation_1", "Re-Run Simulation"),
            ui.br(),

            ui.hr(),
            ui.h4("Simulation Results"),
            ui.h5("Words Rehearsed"),
            ui.output_text_verbatim("rehearsal_words"),
            ui.h5("Words Remembered"),
            ui.output_ui("simulation_1_memory"),
            ui.h5("STM Memory Age Fuzzing Factor over Time"),
            ui.output_plot("fuzz_factors"),
            ui.h5("STM Memory Age over Time"),
            ui.output_plot("rehearsals"),

            ui.h5("Output Trace"),
            ui.output_ui("simulation_1_trace"),

            get_markdown("references"),


        )
    ))


def server(input: Inputs, output: Outputs, session: Session):

    s = reactive.Value(Simulation())

    @reactive.Calc
    def run_simulation_1():
        input.run_simulation_1()

        distraction_level = (input.distraction_level() / 100)
        total_time = input.total_time()

        word_list = [x.strip().lower() for x in input.word_list().split(',')]

        p = ui.Progress()
        p.set(1 / 30, message="Simulating, please wait...")
        s.set(Simulation(word_list))
        infile = Path(__file__).parent / "data/BRM-emot-submit.csv"
        p.set(5 / 30, message="Loading sensory encodings, please wait...")
        s.get().preload(infile)
        p.set(20 / 30, message="Simulating rehearsal over time, please wait...")
        g = ""
        for word_pairs in s.get().run_1(distraction_level, total_time):
            p.set(30 / 30, message="Recalling from short term memory, please wait...")
            g += f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} <br>"
        p.close()

        return g

    @output
    @render.text
    def simulation_1_trace():
        run_simulation_1()
        log = ""
        for line in s.get().data_monitor.trace_log_lines:
            log += f"{line} <br>"
        return log

    @output
    @render.text
    def simulation_1_memory():
        return run_simulation_1()

    @output
    @render.text
    def rehearsal_words():
        return s.get().rehearsal_list

    @output
    @render.ui
    def images() -> ui.Tag:
        img = ui.img(src="Information_Processing_Model_-_Atkinson_&_Shiffrin.jpg", style="width: 400px;")
        return img

    @reactive.Calc
    @output
    @render.plot(alt="Fuzz Factors over Time for Rehearsed Words")
    def fuzz_factors():
        plt.style.use('_mpl-gallery')

        fig, ax = plt.subplots()

        series = s.get().data_monitor.data_for_decay_factors()

        for item, item_series in series.items():
            word = s.get().lookup_word_from_encoding(item)
            if word in s.get().rehearsal_list:
                ax.plot(item_series["xs"], item_series["ys"], linewidth=2.0, label=word)

        ax.legend(loc="upper right")

        return fig

    @reactive.Calc
    @output
    @render.plot(alt="Fuzz Factors over Time for Rehearsed Words")
    def rehearsals():
        plt.style.use('_mpl-gallery')

        fig, ax = plt.subplots()

        series = s.get().data_monitor.rehearsal_points()

        for word, item_series in series.items():
            if word in s.get().rehearsal_list:
                ax.plot(item_series["xs"], item_series["ys"], marker='o', markersize=2.0, label=f"Rehearsal Point - {word}", linestyle='')

        age_series = s.get().data_monitor.word_age()

        for item, item_series in age_series.items():
            word = s.get().lookup_word_from_encoding(item)
            if word in s.get().rehearsal_list:
                ax.plot(item_series["xs"], item_series["ys"], marker="x", label=f"Age - {word}", linestyle='')

        ax.legend(loc="upper right")

        return fig


static_dir = Path(__file__).parent / "report/images"
app = App(app_ui, server, static_assets=static_dir)
