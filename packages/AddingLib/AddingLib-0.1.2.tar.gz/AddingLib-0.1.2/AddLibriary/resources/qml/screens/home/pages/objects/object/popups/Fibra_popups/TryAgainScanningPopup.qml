import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups/" as DS3

DS3.Dialog {
    id: tryAgainScanningPopup

    property var hub: null

    Connections {
        target: hub

        onScan_statusChanged: {
            if (hub.scan_status == "SCAN_STARTED") mainFibraPopup.close()
        }
    }

    title: tr.unable_launch_scan_now_title
    text: tr.unable_launch_scan_now_descr
    isVertical: true
    firstButtonText: tr.try_again_button
    secondButtonText: tr.close
    firstButtonCallback: () => {
        app.hub_management_module.scan_fibra_devices("START")
        isLoading = true
        closeTimer.running = true
        secondButton.enabled = false
        tryAgainScanningPopup.close()
    }
    secondButtonCallback: () => {
        tryAgainScanningPopup.close()
        mainFibraPopup.close()
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