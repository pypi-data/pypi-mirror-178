import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
//  icon source
    property alias icon: iconItem.source
//  text of the badge
    property alias text: textItem.text
//  athena status
    property var status: ui.ds3.status.DEFAULT
//  color defined based on the status
    readonly property var statusColor: ({
        [ui.ds3.status.DEFAULT]: ui.ds3.figure.base,
        [ui.ds3.status.WARNING]: ui.ds3.figure.warningContrast,
        [ui.ds3.status.ATTENTION]: ui.ds3.figure.attention,
        [ui.ds3.status.HAZARD]: ui.ds3.figure.hazard,
        [ui.ds3.status.NOT_IMPORTANT]: ui.ds3.figure.nonessential,
    })[status]

    width: content.width + 16
    height: textItem.height + 4

    radius: 4
    color: ui.ds3.bg.high

    Row {
        id: content

        anchors.centerIn: parent

        spacing: 2

        DS3.Icon {
            id: iconItem

            anchors.verticalCenter: parent.verticalCenter

            color: statusColor
        }

        DS3.Text {
            id: textItem

            anchors.verticalCenter: parent.verticalCenter

            color: statusColor
        }
    }
}
