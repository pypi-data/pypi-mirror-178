from IPython.core.magic import (Magics, line_magic, magics_class)
import requests
import json
from IPython.display import display, Markdown
import ipywidgets as widgets
from ipywidgets import Layout, Button, HBox, VBox
import traceback

@magics_class
class DmtMagic(Magics):
    
    def __init__(self, shell):
        super(DmtMagic, self).__init__(shell)
        
    url = ""
    
    @line_magic("dmtCon")
    def dmtCon(self, line):
        """try:"""
        global url
        url = line
        print  ("Die URL " + url + " wurde hinterlegt!")
        """except:
            traceback.print_exc()"""
            
    @line_magic("dmt")
    def dmt(self, line):
        try:
            if line == "":
                print("FEHLER! Geben sie eine TaskID an!")
            else:
                #line = line.split(' ')
                global url
                dmtUrl = url
                taskID = line
                api_url = dmtUrl + "/dmt/gettaskinfo"
                json = {"taskid": taskID}
                headers =  {"Content-Type":"application/json"}
                response = requests.post(api_url, params=json, headers=headers)
                response = response.json()

                tasktype = response['tasktype']
                status = response['status']
                question = response['question']

                display(Markdown(question))

                button = widgets.Button(description="Abgabe Überprüfen")
                button.style.button_color = 'lightblue'
                button.style.font_weight = 'bold'
                output = widgets.Output()

                if tasktype == "SELECT" or tasktype == "VIEW" or tasktype == "CHECK":
                    input_answer = widgets.Textarea(
                        value='',
                        placeholder='Geben sie Ihren SQL-Code hier ein ...',
                        disabled=False,
                        layout = Layout(width = '800px', height = '100px')
                    )

                    def on_button_clicked_1(b):
                        with output:
                            output.clear_output()

                            answer = input_answer.value
                            api_url = url + "/dmt/gettaskresult"
                            json = {"taskid": taskID, "answer": answer}
                            headers =  {"Content-Type":"application/json"}
                            response = requests.post(api_url, params=json, headers=headers)
                            response = response.json()

                            feedback = response['feedback']
                            points = str(response['points'])
                            pointsMax = str(response['points_max'])

                            print(feedback)
                            print("Punkte: " + points + " / " + pointsMax)

                    display(input_answer)
                    display(Markdown(status))
                    display(button, output)
                    button.on_click(on_button_clicked_1)

                if tasktype == "SCHEMA": 
                    for i in range (6):
                        globals()[f"attribut_{i}"] = widgets.Text(
                            value='',
                            disabled=False
                        )
                        globals()[f"primaer_{i}"] = widgets.Checkbox(
                            value=False,
                            disabled=False,
                            indent=False,
                            layout = Layout(justify_content='center')
                        )
                        globals()[f"fremd_{i}"] = widgets.Checkbox(
                            value=False,
                            disabled=False,
                            indent=False,
                            layout = Layout(justify_content='center')
                        )

                    label_1 = widgets.Label(value="Attributname")
                    label_2 = widgets.Label(value="Primärschlüssel")
                    label_3 = widgets.Label(value="Fremdschlüssel")

                    layout = Layout(width='100%', align_items='center')

                    left = VBox([label_1, attribut_0, attribut_1, attribut_2, attribut_3, attribut_4, attribut_5], layout=layout)
                    middle = VBox([label_2, primaer_0, primaer_1, primaer_2, primaer_3, primaer_4, primaer_5], layout=layout)
                    right = VBox([label_3, fremd_0, fremd_1, fremd_2, fremd_3, fremd_4, fremd_5], layout=layout)
                    box = HBox([left, middle, right])

                    display(box)
                    display(Markdown(status))
                    display(button, output)

                    attributes = [attribut_0, attribut_1, attribut_2, attribut_3, attribut_4, attribut_5]
                    primaer = [primaer_0, primaer_1, primaer_2, primaer_3, primaer_4, primaer_5]
                    fremd = [fremd_0, fremd_1, fremd_2, fremd_3, fremd_4, fremd_5]

                    def on_button_clicked_2(b):
                        with output:
                            output.clear_output()

                            answer = ""

                            for i in range (6):
                                if attributes[i].value != "":
                                    answer += attributes[i].value
                                    answer += "\t"
                                    if primaer[i].value == True:
                                        answer += "1"
                                    else:
                                        answer += "0"
                                    answer += "\t"
                                    if fremd[i].value == True:
                                        answer += "1"
                                    else:
                                        answer += "0"
                                    answer += "\n"

                            api_url = url + "/dmt/gettaskresult"
                            json = {"taskid": taskID, "answer": answer}
                            headers =  {"Content-Type":"application/json"}
                            response = requests.post(api_url, params=json, headers=headers)
                            response = response.json()

                            feedback = response['feedback']
                            points = str(response['points'])
                            pointsMax = str(response['points_max'])

                            print(feedback)
                            print("Punkte: " + points + " / " + pointsMax)

                    button.on_click(on_button_clicked_2)

                if tasktype == "TABLE":

                    for i in range (8):
                          for j in range (5):
                                if i == 0 and j == 0:
                                    globals()[f"cell_{i}{j}"] = widgets.Text(
                                        value='',
                                        placeholder='Attributname...',
                                        disabled=False
                                    )
                                else:
                                    if i == 1 and j == 0:
                                        globals()[f"cell_{i}{j}"] = widgets.Text(
                                            value='',
                                            placeholder='Attributwert...',
                                            disabled=False
                                         )
                                    else:
                                        globals()[f"cell_{i}{j}"] = widgets.Text(
                                            value='',
                                            disabled=False
                                        )

                    head = HBox([cell_00, cell_01, cell_02, cell_03, cell_04])
                    row1 = HBox([cell_10, cell_11, cell_12, cell_13, cell_14])
                    row2 = HBox([cell_20, cell_21, cell_22, cell_23, cell_24])
                    row3 = HBox([cell_30, cell_31, cell_32, cell_33, cell_34])
                    row4 = HBox([cell_40, cell_41, cell_42, cell_43, cell_44])
                    row5 = HBox([cell_50, cell_51, cell_52, cell_53, cell_54])
                    row6 = HBox([cell_60, cell_61, cell_62, cell_63, cell_64])
                    row7 = HBox([cell_70, cell_71, cell_72, cell_73, cell_74])

                    box = VBox([row1, row2, row3, row4, row5, row6, row7])

                    display(head)
                    display(Markdown('<hr style="border:1px solid black">'))
                    display(box) 
                    display(Markdown(status))
                    display(button, output)

                    table = [[cell_00, cell_01, cell_02, cell_03, cell_04],
                             [cell_10, cell_11, cell_12, cell_13, cell_14],
                             [cell_20, cell_21, cell_22, cell_23, cell_24],
                             [cell_30, cell_31, cell_32, cell_33, cell_34],
                             [cell_40, cell_41, cell_42, cell_43, cell_44],
                             [cell_50, cell_51, cell_52, cell_53, cell_54],
                             [cell_60, cell_61, cell_62, cell_63, cell_64],
                             [cell_70, cell_71, cell_72, cell_73, cell_74]]

                    def on_button_clicked_3(b):
                        with output:
                            output.clear_output()

                            answer = ""

                            for i in range (8):
                                for j in range (5):
                                    if table[i][j].value != "":
                                        answer += table[i][j].value
                                    answer += "\t"

                                answer += "\n"

                            api_url = url + "/dmt/gettaskresult"
                            json = {"taskid": taskID, "answer": answer}
                            headers =  {"Content-Type":"application/json"}
                            response = requests.post(api_url, params=json, headers=headers)
                            response = response.json()

                            feedback = response['feedback']
                            points = str(response['points'])
                            pointsMax = str(response['points_max'])

                            print(feedback)
                            print("Punkte: " + points + " / " + pointsMax)

                    button.on_click(on_button_clicked_3)

        except:
            print("FEHLER! Überprüfen sie die angegebene TaskID/URL (%dmtCon) und/oder stellen sie die Verfügbarkeit von DMT sicher!")
            traceback.print_exc()

def load_ipython_extension(ipython):
    ipython.register_magics(DmtMagic)