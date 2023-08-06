import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
    id: buttonNavigation

    property alias text: textItem.text
    property alias icon: icon.source
    property alias mouseArea: mouseArea
    property var color: ui.ds3.figure.interactive
    property bool isIconLeft: true

    signal clicked()

    height: 24
    width: content.width

    opacity: enabled ? 1 : 0.3

    Row {
        id: content

        height: 24

        layoutDirection: isIconLeft ? Qt.LeftToRight : Qt.RightToLeft

        DS3.Icon {
            id: icon

            anchors.verticalCenter: parent.verticalCenter

            color: buttonNavigation.color
            visible: !!source
        }

        DS3.Text {
            id: textItem

            anchors.verticalCenter: parent.verticalCenter

            color: buttonNavigation.color
            style: ui.ds3.text.button.MBold
            visible: !!text
        }
    }

    DS3.MouseArea {
        id: mouseArea

        onClicked: buttonNavigation.clicked()
    }
}
