from puepy import Application, Page, t
import code as kd

app = Application()

@app.page()
class TimeTrackerPage(Page):
    def initial(self):
        t.h2(f"Omkretsen av en sirkel med radius 2 er {kd.omkrets(2)}")
        

    def populate(self):
        t.h1("World!")

app.mount("#app")