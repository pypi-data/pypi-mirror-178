import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property bool isBad: device.antimasking && device.is_masked == 1

    atomTitle {
        title: tr.anti_masking
        subtitle: {
            if (!device.antimasking) { return tr.off }
            if (device.is_masked == "N/A") { return tr.na }
            return (device.is_masked == 1) ? tr.alert : tr.on
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Antimasking-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}