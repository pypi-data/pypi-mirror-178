import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Placeholder text
    property alias placeholder: atomInput.placeholderText
//  If you need text
    property alias atomInput: atomInput
//  To filtrate models
    property alias searchValue: atomInput.text
//  On search icon clicked
    property var find: () => {}
//  If visible spinner (use with function find())
    property bool withSpinner: false
    property alias interval: delaySearch.interval
//  If necessary to change the frame color
    property var frameColor: ui.ds3.bg.high

    width: parent.width
    height: atomInput.height + 24

    color: frameColor

    Rectangle {
        width: atomInput.focus || atomInput.text.length ? parent.width - 48 - cancelButton.width : parent.width - 32
        height: atomInput.height + 16

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 16
            rightMargin: atomInput.focus ? atomInput.contentWidth : 16
        }

        color: atomInput.focus ? ui.ds3.bg.base : ui.ds3.bg.low
        radius: 4

        DS3.ButtonIcon {
            id: searchIcon

            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
                margins: 8
            }

            source: "qrc:/resources/images/Athena/common_icons/Search-M.svg"
            color: ui.ds3.figure.nonessential

            onClicked: {
                find()
            }
        }

        DS3.AtomInput {
            id: atomInput

            width: parent.width

            anchors {
                left: searchIcon.right
                leftMargin: 8
                right: parent.right
                rightMargin: 8 + ( crossButton.visible ? 40 : 0 )
                verticalCenter: parent.verticalCenter
            }

            hasSpinner: withSpinner && delaySearch.running

            onTextEdited: {
                delaySearch.restart()
            }
        }

        DS3.MouseArea {
            id: crossButtonWrapper

            width: 40
            height: parent.height

            anchors {
                right: parent.right
                fill: undefined
            }

            visible: atomInput.text.length && atomInput.focus && !atomInput.hasSpinner && !atomInput.readOnly

            onClicked: {
                atomInput.clear()
                atomInput.textEdited()
            }

            DS3.Icon {
                id: crossButton

                anchors.centerIn: parent

                source: "qrc:/resources/images/Athena/common_icons/InputCross.svg"
            }
        }
    }

    DS3.Text {
        id: cancelButton

        width: contentWidth

        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
            rightMargin: 16
            leftMargin: 16
        }

        style: ui.ds3.text.body.MBold
        text: tr.cancel
        color: ui.ds3.figure.interactive
        visible: atomInput.focus || atomInput.text.length

        DS3.MouseArea {
            onClicked: {
                atomInput.text = ""
                atomInput.focus = false
                find()
            }
        }
    }

    Timer {
        id: delaySearch

        running: false
        interval: 1000

        onTriggered: {
            find()
        }
    }
}
