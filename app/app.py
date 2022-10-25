from PySide2 import QtWidgets
import currency_converter


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.set_default_values()
        self.setup_css()
        self.setup_connections()

    def setup_ui(self):
        # Create layout
        self.layout = QtWidgets.QHBoxLayout(self)
        # Create widgets
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Inverser devices")
        # Add widgets into the layout
        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def setup_css(self):
        self.setStyleSheet("""
            background-color: rgb(26, 27, 37);
            color: white;
        """)
        self.cbb_devisesFrom.setStyleSheet("""
            border: 2px solid white;
            border-radius: 4px;
            padding: 4px 8px;
        """)
        self.cbb_devisesTo.setStyleSheet("""
            border: 2px solid white;
            border-radius: 4px;
            padding: 4px 8px;
        """)
        self.btn_inverser.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 4px;
                padding: 4px 8px;
                color: #1e1e1e;
            }
            QPushButton:hover {
                color: white;
                background-color: blue;
            }
        """)

    def set_default_values(self):
        # Add values into the combo box
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        # Set default values
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")

        self.spn_montant.setRange(1, 1000000000)
        self.spn_montantConverti.setRange(1, 1000000000)

        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    def setup_connections(self):
        # Create signals
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        device_to = self.cbb_devisesTo.currentText()

        try:
            result = self.c.convert(montant, devise_from, device_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'a pas fonctionné.")
        else:
            self.spn_montantConverti.setValue(result)

    def inverser_devise(self):
        devise_from = self.cbb_devisesFrom.currentText()
        device_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(device_to)
        self.cbb_devisesTo.setCurrentText(devise_from)

        self.compute()


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()
