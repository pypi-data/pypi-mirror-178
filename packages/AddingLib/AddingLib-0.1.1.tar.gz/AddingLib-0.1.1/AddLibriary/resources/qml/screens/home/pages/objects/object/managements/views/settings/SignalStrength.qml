import QtQuick 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3

Column {
    width: parent.width


    property var deviceStrength: ["NO_SIGNAL", "WEAK", "NORMAL", "STRONG"].indexOf(device.signal_strength)
    property var rowTitle: device.is_fibra ?
        tr.fibra_signal_strength :
        tr.signal_strength
    property var rowIcon: device.is_fibra ?
        "qrc:/resources/images/Athena/views_icons/Fibra-M.svg" :
        "qrc:/resources/images/Athena/views_icons/Jeweller-M.svg"

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

        visible:  deviceStrength > -1

        atomTitle.title: rowTitle
        leftIcon.source: rowIcon
        atomConnection.strength: deviceStrength
    }
}
