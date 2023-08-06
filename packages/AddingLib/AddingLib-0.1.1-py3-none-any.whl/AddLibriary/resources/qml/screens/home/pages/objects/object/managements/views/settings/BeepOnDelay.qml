import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/desktop/"


AjaxSettingsSwitch {
    id: beepOnDelay
    text: tr.beep_on_delay
    height: 32

    enabled: devEnable
    visible: device.beep_on_delay_available && hub.firmware_version_dec >= 205000
    checked: device.beep_on_delay

    area.onClicked: {
        checked = !checked
    }
}