import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups/" as DS3

DS3.Dialog {
    id: resetEnergyConsumption

    property var device: null
    property var timestamp: 0

    title: tr.energy_consumption_reset_title
    firstButtonText: tr.ok
    secondButtonText: tr.cancel
    firstButtonCallback: () => {
        app.hub_management_module.device_command(device, 22)
    }
}