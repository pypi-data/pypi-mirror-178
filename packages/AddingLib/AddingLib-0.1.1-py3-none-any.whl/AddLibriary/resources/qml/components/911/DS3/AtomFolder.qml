import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3

// Athena 4.6

Item {
//  Folder label text
    property alias labelText: folderLabel.text
//  Text of the badge
    property alias badgeLabel: badge.text
//  If the folder is selected
    property bool isSelected: false
//  source of the icon
    property var iconSource: ""

    width: textRow.width
    height: 40

    Row {
        id: textRow

        anchors.verticalCenter: parent.verticalCenter

        spacing: 4

        DS3.Icon {
            id: icon

            anchors.verticalCenter: parent.verticalCenter

            source: iconSource || ""
            color: folderLabel.color
        }

        DS3.Text {
            id: folderLabel

            anchors.verticalCenter: parent.verticalCenter

            style: ui.ds3.text.button.SBold
            color: ui.ds3.figure[ isSelected ? "interactive" : "secondary" ]
            horizontalAlignment: Text.AlignHCenter
        }

        DS3.BadgeRegular {
            id: badge

            visible: text.length
        }
    }

    Rectangle {
        id: underLine

        width: textRow.width
        height: 1

        anchors.bottom: parent.bottom

        color: ui.ds3.figure.interactive
        visible: isSelected
    }
}
