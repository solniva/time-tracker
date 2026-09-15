from puepy import Application, Page, t
#import utils
import plotting
from puepy.core import html

app = Application()

@app.page()
class TimeTrackerPage(Page):
    def initial(self):
        self.radius = 2
        plotting.make_images()
        return {"dict": "ionary"}
        
    def populate(self):
        #t.h1(f"radiusen er {self.radius} og omkretsen er {utils.omkrets(self.radius)}")
        t(html("<img src='timerA26.png' alt='Bilde' />"))

app.mount("#app")