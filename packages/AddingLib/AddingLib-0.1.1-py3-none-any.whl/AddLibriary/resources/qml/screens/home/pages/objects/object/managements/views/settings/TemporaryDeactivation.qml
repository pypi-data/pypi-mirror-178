import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property bool isBad: !["ENGINEER_BYPASS_OFF", "OFF"].includes(device.bypass_mode)

    visible: hub && hub.firmware_version_dec >= 208107
    atomTitle {
        title: tr.bypass_mode
        subtitle: {
            if (device.is_bypassed == 1) return tr.bypass_on
            if (device.is_bypassed == 2) return tr.bypass_tamper_on
            if (device.is_bypassed == 4 || device.is_bypassed == 6) return tr.bypass_on_automatically_by_numbers
            if (device.is_bypassed == 8 || device.is_bypassed == 10) return tr.bypass_on_automatically
            if (["ENGINEER_BYPASS_OFF", "OFF"].includes(device.bypass_mode)) return tr.no
            return tr.na
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/TemporaryDeactivation-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}