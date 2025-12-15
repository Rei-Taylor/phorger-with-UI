from nicegui import ui, binding as b, run
import pathlib as p
from pkg import file_finder, file_mover, cloud_uploader 

from main import setup
import typing as t
import param as par, asyncio

@b.bindable_dataclass
class AppState:

    mode : t.Literal["Archive", "Cloud"] = "Archive"
    source_path : str = ""
    destination_path : str = ""



class Logger(par.Parameterized):

    logs = par.List(default=[])
    current = par.Dict()
    def __init__(self, **params):
        super().__init__(**params)

    @par.depends('current', watch=True)
    def update_data_on_current_change(self):
        self.logs.append(self.current)
        print(self.logs)
  
        
        

async def runner(state : AppState, debugger : Logger):
    print(f"This is called with {state.mode}")
    setattr(debugger, "current", {"type" : "ACTION", "Message" : f"Running {state.mode} mode"})
    show_log.refresh()
    source_path : str = state.source_path
    target_path : str = state.destination_path
    file_list, size = file_finder(p.Path(source_path))
    print(source_path)
    mode : str = state.mode

    noti = ui.notification(f"Running {mode} mode", position="center", spinner=True, timeout=None)
    if mode == "Archive":
        try:

            print("doing archive mode")
            file_mover(file_list, p.Path(target_path), size, False)
            noti.spinner = False
            noti.message = "Finished"
            await asyncio.sleep(1)
            noti.dismiss()
            debugger.logs.append( {"type" : "SUCCESS", "Message" : f"Successfully Move the {file_list[0].name} to {target_path}"})
        except Exception as e:
            setattr(debugger, "current" , {"type" : "ERROR", "Message" : e})
            show_log.refresh()
            noti.message = "Failed"
            noti.dismiss()
            print(e)
    elif mode == "Cloud":
        try:
            print("doing cloud mode")
            noti.message = f"Using current folders {str(file_list)}"
            await run.io_bound(cloud_uploader,file_list)
            noti.spinner = False
            noti.message = "Finished"
            await asyncio.sleep(1)
            noti.dismiss()
            setattr(debugger, "current", {"type" : "SUCCESS", "Message" : f"Successfully Move the {file_list[0].name} to cloud"})
            show_log.refresh()
            
        except Exception as e:
            setattr(debugger, "current" , {"type" : "ERROR", "Message" : e})
            show_log.refresh()
            noti.message = "Failed"
            noti.dismiss()
            print(e)

    else:
        print("ERROR: invalid mode")         
                   
@ui.refreshable
async def show_log(debugger: Logger):
    css = {"INFO" : "text-blue-300", "ERROR" : "text-red-300", "SUCCESS" : "text-green-300", "ACTION": "Text-amber-300"}

    with ui.card().classes("w-full "):
        with ui.card().classes("w-full h-96 overflow-y-scroll").props("flat outlined bordered"):
            for i in debugger.logs:
                ui.label(f"{i['type']} : {i['Message']}").classes(css[i["type"]])    

@ui.page('/', dark=True)
async def page():

    state = AppState()
    debugger = Logger()
    
    async def on_click():
        await runner(state, debugger)
        
    def on_change(e):
        setattr(debugger, "current", {"type" : "INFO", "Message" : f"Mode changed to {mode_ui.value}"})
        show_log.refresh()
        ui.notification(f"Mode changed to {mode_ui.value}", position="top-right")  

    with ui.header():
        ui.label("Phoger")

    with ui.row(wrap=False).classes("w-full h-96"):
        with ui.card().classes("w-full h-96"):
            with ui.column(align_items="center").classes("w-full"):
                mode_ui = ui.toggle(options=["Archive", "Cloud"]).bind_value(state, "mode")
                mode_ui.on("update:model-value",lambda e :on_change(e))
                source_input = ui.input(label="Source Path").bind_value(state, "source_path").props("rounded filled").classes("w-1/2")
                
                ui.input(label="Destination Path").bind_value(state, "destination_path").props("rounded filled").classes("w-1/2")
                ui.button("Do it", on_click= lambda : on_click())
        
                ui.label().bind_text(state, "mode")
        
        await show_log(debugger=debugger)
   

ui.run(native=True)
        