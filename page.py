from puepy import Application, Page, t

app = Application()

def omkrets(r):
    return 2*r

@app.page()
class TimeTrackerPage(Page):

    def populate(self):
        t.h1("Hello, World!")
        t.h2(f"Omkretsen av en sirkel med radius 2 er {omkrets(2)}")

app.mount("#app")