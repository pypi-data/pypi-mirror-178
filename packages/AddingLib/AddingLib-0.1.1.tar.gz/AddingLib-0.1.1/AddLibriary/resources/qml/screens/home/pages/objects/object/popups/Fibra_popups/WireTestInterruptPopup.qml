import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups

DS3Popups.Dialog {
    id: interruptTestFibraPopup

    property var hub: null

    Connections {
        target: hub

        onMax_power_test_stateChanged: {
            if (hub.max_power_test_state == "TEST_NOT_STARTED") interruptTestFibraPopup.close()
        }
    }

    closePolicy: Popup.NoAutoClose
    title: tr.power_test_in_progress_finish_title
    text: tr.power_test_in_progress_finish_descr
    isVertical: true
    firstButtonText: tr.finish_now_button
    firstButtonCallback: () => {
        app.hub_management_module.device_command(interruptTestFibraPopup.hub, 32)
        isLoading = true
        spinnerItem.hasText = true
        spinnerItem.textItem.text = tr.finishing_progress
        closeTimer.running = true
        secondButton.enabled = false
    }
    secondButtonText: tr.cancel
    secondButtonCallback: () => {
        interruptTestFibraPopup.close()
    }
    autoClose: false

    Timer {
        id: closeTimer

        repeat: false
        running: false
        interval: 1000 * 20 // Popup will always close in 20 seconds

        onTriggered: {
            interruptTestFibraPopup.close()
        }
    }
}