import QtQuick 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3

Column {
    width: parent.width

    property var deviceStrength: ["VERY_LOW", "LOW", "MEDIUM", "HIGH"].indexOf(device.data_channel_signal_quality)
    property var rowTitle: tr.data_channel_signal_strength
    property var rowIcon: "qrc:/resources/images/Athena/views_icons/Wings-M.svg"

    spacing: 1

    DS3.InfoTitle {
        id: infoRow

        width: parent.width

        visible: !infoSignal.visible
        atomTitle {
            title: rowTitle
            subtitle: "N/A"
        }
        leftIcon.source: rowIcon
        status: ui.ds3.status.DEFAULT
    }

    DS3.InfoSignal {
        id: infoSignal

        width: parent.width

        visible: deviceStrength > -1
        atomTitle.title: rowTitle
        leftIcon.source: rowIcon
        atomConnection.strength: return deviceStrength
    }
}