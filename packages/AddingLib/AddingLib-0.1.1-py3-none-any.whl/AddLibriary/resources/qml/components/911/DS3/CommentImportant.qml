import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
// Enum that has all the status types to show the appropriate color for icon
    enum Status {
        Default,        // default
        Warning,
        Attention
    }
//  Status value that accepts the status (should be in the Status enum)
    property var status: DS3.CommentImportant.Status.Default
//  Text of the comment
    property alias atomTitle: atomTitle
//  Icon of the comment
    property alias imageItem: imageItem
    readonly property var colorStatus: {
        switch (status) {
            case DS3.CommentImportant.Status.Default: return ui.ds3.figure.secondary
            case DS3.CommentImportant.Status.Warning: return ui.ds3.figure.warningContrast
            case DS3.CommentImportant.Status.Attention: return ui.ds3.figure.attention
        }
    }

    width: parent.width
    height: Math.max(imageItem.height, atomTitle.height) + 24

    color: ui.ds3.bg.high

    DS3.Icon {
        id: imageItem

        anchors {
            top: parent.top
            topMargin: 16
            left: parent.left
            leftMargin: 16
        }

        color: colorStatus
        source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
        opacity: enabled ? 1 : 0.3
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: imageItem.visible ? 52 : 12
            right: parent.right
            rightMargin: 16
        }

        isPrimary: subtitle
        isBold: isPrimary
        opacity: enabled ? 1 : 0.3
    }

}