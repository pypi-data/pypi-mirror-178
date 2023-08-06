import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups

DS3Popups.Dialog {
    id: popup

    property var close_wizard_action: () => {}

    title: tr.quit_resistance_measurement_title
    text: tr.quit_resistance_measurement_descr
    firstButtonText: tr.continue_
    secondButtonText: tr.quit_now
    isSecondButtonRed: true

    isVertical: true

    firstButtonCallback: () => {
        popup.close()
    }

    secondButtonCallback: () => {
        close_wizard_action()
    }
}