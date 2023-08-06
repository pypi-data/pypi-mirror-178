import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

DS3.DeviceSimple {
    id: deviceSelection

//  Whether selected first button
    property bool firstButtonChecked: false
//  Whether selected second button
    property bool secondButtonChecked: false
//  Whether clicked on first button area
    property alias firstButtonClickedArea: firstButtonClickedArea
//  Whether clicked on second button area
    property alias secondButtonClickedArea: secondButtonClickedArea
//  First button name
    property var firstButtonName
//  Second button name
    property var secondButtonName
//  To disable first button block
    property alias checkItemFirstButton: checkItemFirstButton
//  To disable second button block
    property alias checkItemSecondButton: checkItemSecondButton

    height: textColumn.height + selectionColumn.height + 24
    width: parent.width

    smallImage: true

    deviceImage {
        anchors {
            top: deviceSelection.top
            topMargin: 12
            left: deviceSelection.left
            leftMargin: 12
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
            right: parent.right
            rightMargin: 16
            left: parent.left
            leftMargin: 16
        }

        Rectangle {
            id: firstButtonSeparator

            width: parent.width
            height: 1

            anchors.horizontalCenter: parent.horizontalCenter

            color: ui.ds3.bg.base
        }

        DS3.Spacing {
            height: 1
        }

        Item {
            id: checkItemFirstButton

            width: parent.width
            height: Math.max(firstButtonTitle.height, firstButtonCheck.height) + 16

            DS3.AtomTitle {
                id: firstButtonTitle

                anchors {
                    left: parent.left
                    right: firstButtonCheck.left
                    rightMargin: 8
                    verticalCenter: parent.verticalCenter
                }

                title: firstButtonName
                opacity: enabled ? 1 : 0.3
            }

            Item {
                id: firstButtonCheck

                width: 24
                height: 24

                anchors {
                    right: checkItemFirstButton.right
                    verticalCenter: checkItemFirstButton.verticalCenter
                }

                DS3.SelectMulti {
                    anchors.centerIn: parent

                    checked: deviceSelection.firstButtonChecked
                    opacity: enabled ? 1 : 0.3
                }
            }

            DS3.MouseArea {
                id: firstButtonClickedArea
            }
        }

        Rectangle {
            id: secondButtonSeparator

            width: parent.width
            height: !!secondButtonName ? 1 : 0

            color: ui.ds3.bg.base

            visible: !!secondButtonName

            anchors.horizontalCenter: parent.horizontalCenter
        }

        Item {
            id: checkItemSecondButton

            width: parent.width
            height: !!secondButtonName ? Math.max(secondButtonTitle.height, secondButtonCheck.height) + 16 : 0

            visible: !!secondButtonName

            DS3.AtomTitle {
                id: secondButtonTitle

                anchors {
                    left: parent.left
                    right: secondButtonCheck.left
                    rightMargin: 8
                    verticalCenter: parent.verticalCenter
                }

                title: secondButtonName || ""
                opacity: enabled ? 1 : 0.3
            }

            Item {
                id: secondButtonCheck

                width: 24
                height: 24

                anchors {
                    right: checkItemSecondButton.right
                    verticalCenter: checkItemSecondButton.verticalCenter
                }

                DS3.SelectMulti {
                    anchors.centerIn: parent

                    checked: deviceSelection.secondButtonChecked
                    opacity: enabled ? 1 : 0.3
                }
            }

            DS3.MouseArea {
                id: secondButtonClickedArea
            }
        }
    }
}