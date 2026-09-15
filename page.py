from puepy import Application, Page, t

app = Application()


@app.page()
class TimeTrackerPage(Page):
    r = 2

    def omkrets(r):
        return 2*r
    
    def populate(self, r):
        t.h1("Hello, World!")
        t.h2(f"Omkretsen av en sirkel med radius {r} er {omkrets(r)}")

app.mount("#app")