import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: device.smoke_alarm == 1

    atomTitle {
        title: tr.smoke
        subtitle: {
            if (device.smoke_alarm == "N/A") return tr.na
            return device.smoke_alarm == 1 ? tr.alert : tr.clear
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/SmokeOk-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}