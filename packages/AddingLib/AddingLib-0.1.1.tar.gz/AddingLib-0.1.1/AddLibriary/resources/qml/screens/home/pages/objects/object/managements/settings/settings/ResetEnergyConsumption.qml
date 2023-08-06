import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.ButtonRow {
    text: tr.reset_energy_consumption
    rowLeftAlign: true

    onClicked: {
        Popups.popupByPath(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/socket_base_popups/ResetEnergyConsumption.qml",
            {"device": device}
        )
    }
}