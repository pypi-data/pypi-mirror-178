import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Status value that accepts the status (should be in the Status enum)
    property var status: ui.ds3.status.DEFAULT
//  Left icon
    property alias leftIcon: leftIcon
//  Main text
    property alias atomTitle: atomTitle
//  Is the element enabled (because if we use "enabled" it causes the whole component to become unacceseble and
//  there are cases where we need to disable only text and not the whole element)
    property bool stateEnabled: true
//  The maping of status to color
    readonly property var statusColor: ({
        [ui.ds3.status.DEFAULT]: ui.ds3.figure.base,
        [ui.ds3.status.WARNING]: ui.ds3.figure.warningContrast,
        [ui.ds3.status.ATTENTION]: ui.ds3.figure.attention,
        [ui.ds3.status.HAZARD]: ui.ds3.figure.hazard,
        [ui.ds3.status.NOT_IMPORTANT]: ui.ds3.figure.nonessential,
    })[status]

    implicitWidth: parent.width
    height: atomTitle.height + 24

    color: ui.ds3.figure.transprent

    DS3.Icon {
        id: leftIcon

        width: 24
        height: 24

        anchors {
            left: parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
        }

        opacity: stateEnabled ? 1 : 0.3
        color: ui.ds3.figure.base
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: leftIcon.source != '' ? leftIcon.right : parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        isPrimary: !atomTitle.subtitle
        subtitleColor: statusColor || ui.ds3.figure.base
        opacity: stateEnabled ? 1 : 0.3
    }
}
