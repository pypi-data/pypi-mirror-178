import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    // The flow icons model
    property alias flowIconsModel: repeater.model

    width: childrenRect.width
    height: 16

    Row {
        spacing: 8

        Repeater {
            id: repeater
            model: device.status_icons_list

            DS3.Icon {
                id: imageItem

                source: repeater.model[index].source
                color: ui.ds3.figure[repeater.model[index].color]
            }
        }
    }
}