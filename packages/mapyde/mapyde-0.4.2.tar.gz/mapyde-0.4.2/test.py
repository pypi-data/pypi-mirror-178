from rich.console import Console
import os

class ConsolePanel(Console):
    def __init__(self,*args,**kwargs):
        console_file = open(os.devnull,'w')
        super().__init__(record=True,file=console_file,*args,**kwargs)

    def __rich_console__(self,console,options):
        texts = self.export_text(clear=False).split('\n')
        for line in texts[-options.height:]:
            yield line

if __name__=='__main__':
    from rich.layout import Layout
    from rich.live import Live
    import time
    from datetime import datetime
    class Interface():
        def __init__(self) -> None:
            self.console:list[ConsolePanel] = [ConsolePanel() for _ in range(2)]

        def get_renderable(self):
            layout = Layout()
            layout.split_column(
                Layout(self.console[0],name='top'),
                Layout(self.console[1],name='bottom',size=6)
            )
            layout.children[0]
            return layout

    db = Interface()
    with Live(get_renderable=db.get_renderable):
        while True:
            time.sleep(1)
            db.console[0].print(datetime.now().ctime()+'='*100)
            db.console[1].print(datetime.now().ctime())
