import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: device.alarm_co == 1

    visible: device.co_alarms_enabled
    atomTitle {
        title: tr.high_co_level
        subtitle: {
            if (device.alarm_co == "N/A") return tr.na
            return device.alarm_co == 1 ? tr.alert : tr.no
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/CoLevel-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}