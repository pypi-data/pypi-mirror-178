import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

DS3.DeviceSimple {
    id: deviceSelection

//  Whether selected button
    property bool buttonChecked: false
//  Whether clicked on button area
    property alias buttonClickArea: buttonClickArea
//  Button name
    property var buttonName
//  To disable the button block
    property alias checkItemButton: checkItemButton

    height: textColumn.height + selectionColumn.height + 24

    smallImage: true
    deviceImage {
        anchors {
            top: deviceSelection.top
            topMargin: 12
            left: deviceSelection.left
            leftMargin: 16
            verticalCenter: undefined
        }
    }
    textColumn {
        anchors {
            verticalCenter: undefined
            top: deviceSelection.top
            topMargin: 10
        }
    }

    Column {
        id: selectionColumn

        width: parent.width

        anchors {
            top: textColumn.bottom
            topMargin: 12
            horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            width: parent.width - 32
            height: 1

            anchors.horizontalCenter: parent.horizontalCenter

            color: ui.ds3.bg.base
        }

        DS3.Spacing {
            height: 1
        }

        Item {
            id: checkItemButton

            width: parent.width
            height: Math.max(buttonTitle.height, buttonCheck.height) + 16

            DS3.AtomTitle {
                id: buttonTitle

                anchors {
                    left: parent.left
                    leftMargin: 16
                    right: buttonCheck.left
                    rightMargin: 8
                    verticalCenter: parent.verticalCenter
                }

                title: buttonName
                opacity: enabled ? 1 : 0.3
            }

            Item {
                id: buttonCheck

                width: 30
                height: 30

                anchors {
                    right: checkItemButton.right
                    rightMargin: 16
                    verticalCenter: checkItemButton.verticalCenter
                }

                DS3.SelectMulti {
                    anchors.centerIn: parent

                    checked: deviceSelection.buttonChecked
                    opacity: enabled ? 1 : 0.3
                }
            }

            DS3.MouseArea {
                id: buttonClickArea
            }
        }
    }
}
