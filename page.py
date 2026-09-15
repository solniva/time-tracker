from puepy import Application, Page, t
import code as kd

app = Application()

@app.page()
class TimeTrackerPage(Page):

    def populate(self):
        t.h1("Hello, World!")
        t.h2(f"Omkretsen av en sirkel med radius 2 er {kd.omkrets(2)}")

app.mount("#app")