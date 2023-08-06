import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups/" as DS3

DS3.Dialog {
    id: exitScannedDevices

    property var hub: null

    Connections {
        target: hub

        onScan_statusChanged: {
            if (hub.scan_status == "SCAN_NOT_STARTED") mainFibraPopup.close()
        }
    }

    title: tr.add_bus_device_wizard_exit_title
    text: tr.add_bus_device_wizard_exit_descr
    isVertical: true
    firstButtonText: tr.exit_button
    secondButtonText: tr.back
    firstButtonCallback: () => {
        app.hub_management_module.scan_fibra_devices("STOP")
        isLoading = true
        spinnerItem.hasText = true
        spinnerItem.textItem.text = tr.finishing_progress
        closeTimer.running = true
        secondButton.enabled = false
    }
    secondButtonCallback: () => {
        exitScannedDevices.close()
    }
    autoClose: false

    Timer {
        id: closeTimer

        repeat: false
        running: false
        interval: 1000 * 20 // Popup will always close in 20 seconds

        onTriggered: {
            fibraScanningInterruptPopup.close()
        }
    }
}