import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    id: inputResistanceCombobox

    property var resistances: util.get_resistance()

    atomTitle.title: tr.input_resistance
    model: resistances.map((elem) => elem + " " + tr.resistance_value)
    currentIndex: resistances.indexOf((device.input_resistance / 10).toFixed(1))
}