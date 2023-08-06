import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property bool isBad: device.leak_detected == 1

    atomTitle {
        title: tr.leak_detected
        subtitle: {
            if (device.leak_detected == "N/A") return tr.na
            if (device.leak_detected == 1) {
                return tr.yes
            }
            return tr.no
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Leakage-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}