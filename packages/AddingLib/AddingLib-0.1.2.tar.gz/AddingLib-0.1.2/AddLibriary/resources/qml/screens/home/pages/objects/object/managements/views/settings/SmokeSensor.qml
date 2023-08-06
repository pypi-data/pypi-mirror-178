import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: device.camera_malfunction == 1

    atomTitle {
        title: tr.smoke_sensor
        subtitle: {
            if (device.camera_malfunction == "N/A") return tr.na
            return device.camera_malfunction == 1 ? tr.malfunction : tr.ok
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/SmokeSensor-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}