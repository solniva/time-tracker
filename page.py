from puepy import Application, Page, t
import utils

app = Application()

@app.page()
class TimeTrackerPage(Page):
    def initial(self):
        self.radius = 2
        return {"dict": "ionary"}
        
    def populate(self):
        t.h1(f"radiusen er {self.radius} og omkretsen er {utils.omkrets(self.radius)}")

app.mount("#app")