import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups

DS3Popups.Dialog {
    id: fibraScanningInterruptPopup

    property var hub: null

    Connections {
        target: hub

        onScan_statusChanged: {
            if (hub.scan_status == "SCAN_NOT_STARTED") fibraScanningInterruptPopup.close()
        }
    }

    closePolicy: Popup.NoAutoClose
    title: tr.interrupt_scanning_proceed_title
    text: tr.interrupt_scanning_proceed_descr
    isVertical: true
    firstButtonText: tr.interrupt_scanning_proceed_button
    firstButtonCallback: () => {
        app.hub_management_module.scan_fibra_devices("STOP")
        isLoading = true
        spinnerItem.hasText = true
        spinnerItem.textItem.text = tr.finishing_progress
        closeTimer.running = true
        secondButton.enabled = false
    }
    secondButtonText: tr.cancel
    secondButtonCallback: () => {
        fibraScanningInterruptPopup.close()
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