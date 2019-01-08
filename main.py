from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import sys

class WarframeTradingTextGenerator(QWidget):
    update = pyqtSignal()
    update_output = pyqtSignal()
    copy = pyqtSignal()

    items_max = 10
    riven_items_column = 0
    veiled_items_column = 2
    vertical_dividers = [1, 4]
    extended_vertical_dividers = [0, 1]

    def __init__(self):
        super().__init__()
        try:
            with open('data.json') as f:
                self.data = json.load(f)
        except:
            print("read error")
            self.data = {
                "buying" : 0,
                "selling" : 0,
                "other": {},
                "output": "",
                "unrolled": [
                ],
                "veiled_buying": {
                    "Kitgun": [
                        0,
                        "50"
                    ],
                    "Melee": [
                        0,
                        "50"
                    ],
                    "Pistol": [
                        0,
                        "20"
                    ],
                    "Rifle": [
                        0,
                        "50"
                    ],
                    "Zaw": [
                        0,
                        "20"
                    ]
                },
                "wtb_first": 0
            }

        glayout = QGridLayout()
        self.veiled_type = [QCheckBox() for i in range(0, self.items_max)]
        self.veiled_prices = [QLineEdit() for i in range(0, self.items_max)]
        self.weapons = [QLineEdit() for i in range(0, self.items_max)]
        self.lines = [QFrame() for i in range(0, len(self.vertical_dividers))]
        self.other_check_buy = [QCheckBox() for i in range(0, self.items_max-1)]
        self.other_check_sell = [QCheckBox() for i in range(0, self.items_max-1)]
        self.other_name = [QLineEdit() for i in range(0, self.items_max-1)]
        self.other_price = [QLineEdit() for i in range(0, self.items_max-1)]

        #top banner
        self.buying = QCheckBox('Buying')
        self.buying.setChecked(self.data.get("buying", 0))
        self.selling = QCheckBox('Selling')
        self.selling.setChecked(self.data.get("selling", 0))
        self.output = QTextEdit()
        self.output.setText(self.data["output"])
        self.wtb_first = QCheckBox("WTB First")
        self.copy_button = QPushButton("Copy")
        if self.data.get("wtb_first", 0):
            self.wtb_first.setChecked(0)

        glayout.addWidget(self.buying, 2, self.veiled_items_column, 1, 1)
        glayout.addWidget(self.selling, 2, self.riven_items_column, 1, 1)
        glayout.addWidget(self.output, 0, 0, 2, 9)
        glayout.addWidget(self.wtb_first, 1, 9, 1, 1)
        glayout.addWidget(self.copy_button, 0, 9, 1, 1)


        # buying 1 : veiled rivnes
        i = 0
        for key, value in self.data.get("veiled_buying").items():
            glayout.addWidget(self.veiled_type[i], i+3, self.veiled_items_column, 1, 1)
            glayout.addWidget(self.veiled_prices[i], i+3, self.veiled_items_column+1, 1, 1)
            self.veiled_type[i].setText(key)
            self.veiled_prices[i].setText(str(value[1]))
            if value[0]:
                self.veiled_type[i].setChecked(1)
            i = i +1

        # selling : unrolled
        for x in range(0, self.items_max):
            glayout.addWidget(self.weapons[x], x+3, self.riven_items_column, 1, 1)
        unrolled = self.data.get("unrolled")
        for i in range(0, len(unrolled)):
            self.weapons[i].setText(unrolled[i])
        for i in range(len("unrolled")+1,self.items_max):
            self.weapons[i].setText("")

        # other
        self.buy_label_other = QLabel("Buy")
        self.sell_label_other = QLabel("Sell")
        self.name_label_other = QLabel("Name")
        self.price_label_other = QLabel("Price")
        glayout.addWidget(self.buy_label_other, 2, 6, 1, 1)
        glayout.addWidget(self.sell_label_other, 2, 7, 1, 1)
        glayout.addWidget(self.name_label_other, 2, 8, 1, 1)
        glayout.addWidget(self.price_label_other, 2, 9, 1, 1)
        for i in range(0, len(self.other_check_buy)):
            glayout.addWidget(self.other_check_buy[i], i+3, 6, 1, 1)
            glayout.addWidget(self.other_check_sell[i], i+3, 7, 1, 1)
            glayout.addWidget(self.other_name[i], i+3, 8, 1, 1)
            glayout.addWidget(self.other_price[i], i+3, 9, 1, 1)
        i = 0
        for item, value in self.data["other"].items():
            self.other_name[i].setText(item)
            self.other_price[i].setText(value[1])
            if value[0] == "b":
                self.other_check_buy[i].setChecked(1)
            elif value[0] == "s":
                self.other_check_sell[i].setChecked(1)
            elif value[0] == "x":
                pass
            else:
                print("bad json value, b or s in other")
            i = i + 1

        #vertical lines
        for i in range(0, len(self.vertical_dividers)):
            if i in self.extended_vertical_dividers:
                glayout.addWidget(self.lines[i], 2, self.vertical_dividers[i], self.items_max+1, 1)
            else:
                glayout.addWidget(self.lines[i], 3, self.vertical_dividers[i], self.items_max, 1)

        for checkbox in self.veiled_type:
            checkbox.clicked.connect(self.update)
        for line in self.veiled_prices:
            line.textChanged.connect(self.update)
        for line in self.weapons:
            line.textChanged.connect(self.update)
        for i in range(0, len(self.vertical_dividers)):
            self.lines[i].setFrameShape(QFrame.VLine)
        for checkbox in self.other_check_buy:
            checkbox.clicked.connect(self.update)
        for checkbox in self.other_check_sell:
            checkbox.clicked.connect(self.update)
        for line in self.other_name:
            line.textChanged.connect(self.update)
        for line in self.other_price:
            line.textChanged.connect(self.update)
        self.buying.clicked.connect(self.update)
        self.selling.clicked.connect(self.update)
        self.output.textChanged.connect(self.update_output)
        self.wtb_first.clicked.connect(self.update)
        self.copy_button.clicked.connect(self.copy)


        self.setLayout(glayout)
        self.show()
        self.setWindowTitle('WarframeTradingTextGenerator')
        self.check_output_size()
        try:
            f.close()
        except:
            pass

    def update(self):
        self.output.blockSignals(1)

        # buying
        buying_text = ""
        self.data["buying"] = self.buying.isChecked()
        if self.buying.isChecked():
            parsed = []
            for i in range(0, len(self.veiled_type)):
                if self.veiled_type[i].isChecked() == 0 or self.veiled_type[i].text() == "":
                    parsed.append(i)
                    if self.veiled_type[i].text() != "":
                        self.data["veiled_buying"][self.veiled_type[i].text()] = [0, self.veiled_prices[i].text()]

            for i in range(0, len(self.veiled_type)):
                if i in parsed:
                    continue
                parsed.append(i)
                typetext = self.veiled_type[i].text()
                price = self.veiled_prices[i].text()
                self.data["veiled_buying"][self.veiled_type[i].text()] = [1, price]

                for x in range(i, len(self.veiled_type)):
                    if x in parsed or self.veiled_prices[x].text() != price:
                        continue
                    parsed.append(x)
                    self.data["veiled_buying"][self.veiled_type[x].text()] = [1, price]
                    typetext += "/" + self.veiled_type[x].text()

                buying_text += typetext + " " + price + "p, "

        # selling
        selling_text = "unrolled "
        self.data["unrolled"] = []
        self.data["selling"] = self.selling.isChecked()
        for line in self.weapons:
            if line.text() == "":
                continue
            selling_text += "[" + line.text() + "]"
            self.data["unrolled"].append(line.text())
        selling_text += ","
        if selling_text == "unrolled ," or self.selling.isChecked() == 0:
            selling_text = ""

        # Parse Others
        self.data["other"] = {}
        for i in range(0, len(self.other_check_buy)):
            self.data["other"][self.other_name[i].text()] = ["x", self.other_price[i].text()]
            if self.other_check_buy[i].isChecked() and self.other_check_sell[i].isChecked():
                self.other_check_buy[i].setChecked(0)
                self.other_check_sell[i].setChecked(0)
                continue
            if self.other_check_sell[i].isChecked() == 0 and self.other_check_buy[i].isChecked() == 0:
                if self.other_name[i].text():
                    self.data["other"][self.other_name[i].text()] = ["x", self.other_price[i].text()]
                else:
                    try:
                        del self.data["other"][""]
                    except:
                        pass
                continue
            if self.other_check_buy[i].isChecked() and self.other_price[i].text() and self.other_name[i].text():
                buying_text = self.other_name[i].text() + " " + self.other_price[i].text() + "p, " + buying_text
                self.data["other"][self.other_name[i].text()] = ["b", self.other_price[i].text()]
            elif self.other_check_sell[i].isChecked() and self.other_price[i].text() and self.other_name[i].text():
                selling_text = self.other_name[i].text() + " " + self.other_price[i].text() + "p, " + selling_text
                self.data["other"][self.other_name[i].text()] = ["s", self.other_price[i].text()]
            else:
                self.data["other"][self.other_name[i].text()][0] = "b" if self.other_check_buy[i].isChecked() else "s"

        # how to arrange everything
        if self.buying.isChecked() == 0:
            output_text = "WTS " + selling_text
        elif self.selling.isChecked() == 0:
            output_text = "WTB " + buying_text
        elif self.wtb_first.isChecked():
            output_text = "WTB " + buying_text + " WTS " + selling_text
        else:
            output_text = "WTS " + selling_text + " WTB " + buying_text
        if output_text.endswith(" "):
            output_text = output_text[:-1]
        if output_text.endswith(","):
            output_text = output_text[:-1]
        if self.buying.isChecked() == 0 and self.selling.isChecked() == 0:
            output_text = ""

        self.output.setText(output_text)
        self.data["output"] = output_text

        with open("data.json", "w") as f:
            json.dump(self.data, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()
        self.check_output_size()
        self.output.blockSignals(0)

    def update_output(self):
        self.data["output"] = self.output.toPlainText()
        with open("data.json", "w") as f:
            json.dump(self.data, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()
        self.check_output_size()

    def check_output_size(self):
        if len(self.data["output"]) > 120:
            self.copy_button.setText("MAX CHARACTERS, " + str(len(self.data["output"])-120) + " over")
            self.copy_button.setEnabled(0)
        else:
            self.copy_button.setText("Copy")
            self.copy_button.setEnabled(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = WarframeTradingTextGenerator()
    w.resize(800, 800)
    sys.exit(app.exec_())

