import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
//  Folder label text
    property alias labelText: folderLabel.text
//  Text of the badge
    property alias badgeLabel: badge.text
//  If the folder is selected
    property bool selected: false

    width: folderLabel.contentWidth + ( badge ? badge.width * 2 : 0 )
    height: 40

    Row {
        id: textRow

        anchors {
            top: parent.top
            topMargin: 10
        }

        spacing: 4

        DS3.Text {
            id: folderLabel

            style: ui.ds3.text.button.SBold
            color: ui.ds3.figure[ selected ? "interactive" : "secondary" ]
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        DS3.BadgeLabel {
            id: badge

            radius: width / 2
            visible: text.length
        }
    }

    Rectangle {
        width: textRow.width
        height: 1

        anchors {
            top: textRow.bottom
            topMargin: 9
        }

        color: ui.ds3.figure.interactive
        visible: selected
    }
}
