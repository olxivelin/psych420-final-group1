from pathlib import Path
from shiny import Inputs, Outputs, Session, App, reactive, render, ui
import matplotlib.pyplot as plt

from report_helpers import rendering
from report_helpers.rendering import get_markdown
from simulation import Simulation

report_path = Path(__file__).parent / "report"

app_ui = ui.page_fluid(
    ui.panel_title('Memory Simulation'),  # 1
    # ui.layout_sidebar(
    #     ui.panel_sidebar(
    #     ),
    ui.panel_main(
        get_markdown("background", report_path),
        get_markdown("atkinson_shiffrin_model", report_path),
        ui.output_ui(id="images"),
        # get_markdown("sensory_memory", report_path),
        # get_markdown("short_term_memory", report_path),
        # get_markdown("long_term_memory", report_path),
        # get_markdown("learning"),
        get_markdown("our_model", report_path),

        get_markdown("simulation_1", report_path),
        ui.br(),
        ui.input_slider(id="distraction_level", label="Distraction Level", value=20, min=0, max=100),
        ui.input_slider(id="rehearsal_interval", label="Rehearsal Interval (s)", value=10, min=0, max=100),
        ui.input_slider(id="fuzzy_threshold", label="Fuzziness Threshold", value=3, min=0, max=1000),
        ui.input_numeric(id="total_time", label="Simulation Time Length (s)", value=100, min=0, max=10000),
        ui.input_select(id="purge_strategy", label="STM Purge Strategy", choices=("oldest", "weakest")),
        ui.input_text(id="word_list", label="Words to Rehearse", value="person, man, woman, camera, tv"),
        ui.input_action_button("run_simulation_1", "Re-Run Simulation"),
        # ui.input_action_button("toggle_trace", "Toggle Trace Log"),
        ui.br(),
        ui.hr(),
        ui.h4("Simulation Results"),
        ui.h5("Words Rehearsed"),
        ui.output_text_verbatim("rehearsal_words"),

        ui.h5("Words Recalled from STM"),
        ui.output_text_verbatim("simulation_1_recall"),

        ui.h5("Original Words Remembered from LTM"),
        ui.output_text_verbatim("simulation_1_memory"),

        ui.h5("STM Memory Age Fuzzing Factor over Time"),
        ui.output_plot("simulation_1_fuzz_factors"),
        ui.h5("STM Memory Age over Time"),
        ui.output_plot("simulation_1_rehearsals"),
        ui.h5("Max Ages"),
        ui.output_plot("simulation_1_max_ages"),
        ui.h5("Output Trace", id="s1-trace-header"),
        ui.output_ui("simulation_1_trace"),

        ui.br(), ui.br(),
        ui.hr(), ui.hr(),
        ui.br(), ui.br(),

        get_markdown("simulation_2", report_path),
        ui.br(),
        ui.input_numeric(id="s2_total_time", label="Simulation Time Length (s)", value=5, min=0, max=100),
        ui.input_slider(id="s2_fuzzy_threshold", label="Fuzziness Threshold", value=3, min=0, max=1000),
        ui.input_select(id="s2_purge_strategy", label="STM Purge Strategy", choices=("oldest", "weakest")),
        ui.input_text(id="s2_word_list", label="Words to Rehearse", value="person, man, woman, camera, tv"),
        ui.input_action_button("run_simulation_2", "Re-Run Simulation"),
        ui.br(),
        ui.hr(),
        ui.h4("Simulation 2 Results"),
        ui.h5("Words To Remember"),
        ui.output_text_verbatim("simulation_2_rehearsal_words"),
        ui.h5("Recalled from Short Term Memory"),
        ui.output_text_verbatim("simulation_2_recall"),
        ui.h5("STM Memory Age Fuzzing Factor over Time"),
        ui.output_plot("simulation_2_fuzz_factors"),
        ui.h5("Word Fuzziness in STM over Time"),
        ui.output_plot("simulation_2_decayed_word_factors"),
        ui.h5("Max Ages"),
        ui.output_plot("simulation_2_max_ages"),
        ui.h5("Output Trace", id="s2-trace-header"),
        # ui.input_action_button("s2_toggle_trace", "Toggle Trace Log"),
        ui.output_ui("simulation_2_trace"),

        ui.hr(),
        get_markdown("references", report_path),

    )
    # )
)


def server(input: Inputs, output: Outputs, session: Session):

    s = reactive.Value(Simulation())
    s2 = reactive.Value(Simulation())

    @reactive.Effect
    def run_simulation_1():
        input.run_simulation_1()

        distraction_level = (input.distraction_level() / 100)
        fuzziness_threshold = (input.fuzzy_threshold() / 1000)
        total_time = input.total_time()
        purge_strategy = input.purge_strategy()

        word_list = [x.strip().lower() for x in input.word_list().split(',')]

        p = ui.Progress()
        p.set(1 / 30, message="Simulating, please wait...")
        s.set(Simulation(word_list))
        infile = Path(__file__).parent / "data/BRM-emot-submit.csv"
        p.set(5 / 30, message="Loading sensory encodings, please wait...")
        s.get().preload(infile)
        s.get().set_stm_purge_strategy(purge_strategy)
        p.set(20 / 30, message="Simulating rehearsal over time, please wait...")
        g = ""
        for word_pairs in s.get().run_1(distraction_level=distraction_level,
                                        total_time=total_time,
                                        fuzzy_threshold=fuzziness_threshold):
            p.set(30 / 30, message="Recalling from short term memory, please wait...")
            g += f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} <br>"
        p.close()

        return g

    @output
    @render.text
    def simulation_1_trace():
        log = ""
        for line in s.get().data_monitor.trace_log_lines:
            log += f"{line} <br>"
        return log

    # @reactive.Effect
    # def _():
    #     btn = input.toggle_trace()
    #     if btn % 2 == 1:
    #         trace = ui.output_ui(
    #             "simulation_1_trace", simulation_1_trace(), 0, 100, 20
    #         )
    #         ui.insert_ui(
    #             ui.div({"id": "s1-trace"}, trace),
    #             selector="#s1-trace-header",
    #             where="afterEnd",
    #         )
    #     elif btn > 0:
    #         ui.remove_ui("#s1-trace")

    @output
    @render.text
    def simulation_1_memory():
        return rendering.render_recalled_words(s.get().remember_from_ltm())

    @output
    @render.text
    def simulation_1_recall():
        return rendering.render_recalled_words(s.get().recall_from_stm())

    @output
    @render.text
    def rehearsal_words():
        return s.get().rehearsal_list

    @output
    @render.ui
    def images() -> ui.Tag:
        img = ui.img(src="Information_Processing_Model_-_Atkinson_&_Shiffrin.jpg", style="width: 400px;")
        return img

    @output
    @render.plot(alt="Fuzz Factors over Time for Rehearsed Words")
    def simulation_1_fuzz_factors():
        plt.style.use('_mpl-gallery')

        fig, ax = plt.subplots()

        series = s.get().data_monitor.data_for_decay_factors()

        for item, item_series in series.items():
            word = s.get().lookup_word_from_encoding(item)
            if word in s.get().rehearsal_list:
                ax.plot(item_series["xs"], item_series["ys"], linewidth=2.0, label=word)

        ax.legend(loc="upper right")

        return fig

    @output
    @render.plot(alt="Fuzz Factors over Time for Rehearsed Words")
    def simulation_1_rehearsals():
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

    @output
    @render.plot(alt="Max Ages for Words in STM")
    def simulation_1_max_ages():
        plt.style.use('_mpl-gallery')

        x = s.get().data_monitor.max_ages

        fig, ax = plt.subplots()
        ax.hist(x)
        return fig

    @reactive.Effect
    def run_simulation_2():
        input.run_simulation_2()

        distraction_level = 0
        fuzziness_threshold = (input.s2_fuzzy_threshold() / 1000)
        total_time = input.s2_total_time()
        purge_strategy = input.s2_purge_strategy()

        word_list = [x.strip().lower() for x in input.s2_word_list().split(',')]

        p = ui.Progress()
        p.set(1 / 30, message="Simulating, please wait...")
        s2.set(Simulation(word_list))
        infile = Path(__file__).parent / "data/BRM-emot-submit.csv"
        p.set(5 / 30, message="Loading sensory encodings, please wait...")
        s2.get().preload(infile)
        s2.get().set_stm_purge_strategy(purge_strategy)
        p.set(20 / 30, message="Simulating time passing, please wait...")
        g = ""
        for word_pairs in s2.get().run_2(distraction_level=distraction_level, total_time=total_time, fuzzy_threshold=fuzziness_threshold):
            p.set(30 / 30, message="Recalling from short term memory, please wait...")
            g += f"Input: {word_pairs[0]} Recalled: {word_pairs[1]} Strength: {word_pairs[2]} <br>"
        p.close()

        return g

    @output
    @render.text
    def simulation_2_recall():
        return rendering.render_recalled_words(s2.get().recall_from_stm())

    @output
    @render.text
    def simulation_2_trace():
        log = ""
        for line in s2.get().data_monitor.trace_log_lines:
            log += f"{line} <br>"
        return log

    # @reactive.Effect
    # def _():
    #     btn = input.toggle_trace()
    #     if btn % 2 == 1:
    #         trace = ui.output_ui(
    #             "simulation_2_trace", simulation_2_trace(), 0, 100, 20
    #         )
    #         ui.insert_ui(
    #             ui.div({"id": "s2-trace"}, trace),
    #             selector="#s2-trace-header",
    #             where="afterEnd",
    #         )
    #     elif btn > 0:
    #         ui.remove_ui("#s2-trace")

    @output
    @render.text
    def simulation_2_rehearsal_words():
        return s2.get().rehearsal_list

    @output
    @render.plot(alt="Fuzz Factors over Time for Rehearsed Words")
    def simulation_2_fuzz_factors():
        plt.style.use('_mpl-gallery')

        fig, ax = plt.subplots()

        series = s2.get().data_monitor.data_for_decay_factors()

        for item, item_series in series.items():
            word = s2.get().lookup_word_from_encoding(item)
            if word in s2.get().rehearsal_list:
                ax.plot(item_series["xs"], item_series["ys"], linewidth=2.0, label=word)

        ax.legend(loc="upper right")

        return fig

    @output
    @render.plot(alt="Decayed Valence for Words")
    def simulation_2_decayed_word_factors():
        plt.style.use('_mpl-gallery')

        fig, ax = plt.subplots()

        series = s2.get().data_monitor.decayed_word_factors()

        for item, item_series in series.items():
            word = s2.get().lookup_word_from_encoding(item)
            ax.plot(item_series["xs"], item_series["valence"], linewidth=1.0, label=f"Valence ({word})")
            ax.plot(item_series["xs"], item_series["arousal"], linewidth=1.0, label=f"Arousal ({word})")
            ax.plot(item_series["xs"], item_series["dominance"], linewidth=1.0, label=f"Dominance ({word})")

        ax.legend(loc="upper right")

        return fig

    @output
    @render.plot(alt="Max ages for words in STM")
    def simulation_2_max_ages():
        plt.style.use('_mpl-gallery')

        x = s2.get().data_monitor.max_ages

        fig, ax = plt.subplots()
        ax.hist(x)
        return fig


static_dir = Path(__file__).parent / "report/images"
app = App(app_ui, server, static_assets=static_dir)
