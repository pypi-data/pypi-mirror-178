import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


// Regular button
Button {
    id: buttonRegular

//  color of button background
    property var color: ui.ds3.figure.interactive
//  the view of button (if outline, then background is transparent)
    property var isOutline: false
//  does the button icon on the right
    property var isIconRight: false
//  does the button icon on the left
    property var isIconLeft: false
//  maximum width of the button
    property var maxWidth
//  source of the icon
    property var buttonIconSource: ""

    width: content.width + 64
    height: 48

    background: Rectangle {
        radius: height
        color: isOutline ? ui.ds3.figure.transparent : buttonRegular.color
        opacity: !enabled ? 0.3 : (pressed ? 0.6 : 1)
        border.color: buttonRegular.color

        anchors.fill: parent
    }

    contentItem: Item {
        Row {
            id: content

            onWidthChanged: if (content.width + 64 > buttonRegular.maxWidth) {
                buttonText.width -= (content.width + 64 - buttonRegular.maxWidth)
            }

            height: parent.height

            spacing: 5

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter

//            DS3.Icon {
//                visible: isIconLeft
//
//                iconSource: buttonIconSource
//                color: buttonText.color
//                opacity: background.opacity
//
//                anchors {
//                    verticalCenter: parent.verticalCenter
//                }
//            }

            DS3.Text {
                id: buttonText

                width: undefined

                text: buttonRegular.text
                style: ui.ds3.text.body.MBold
                font.letterSpacing: 0.7
                color: isOutline ? background.border.color : ui.ds3.figure.inverted
                opacity: background.opacity
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                hasElide: true

                anchors.verticalCenter: parent.verticalCenter

                Component.onCompleted: if (content.width + 64 > buttonRegular.width) {
                    width -= content.width + 64 - buttonRegular.width
                }
            }

//            Icon {
//                visible: isIconRight
//
//                iconSource: buttonIconSource
//                color: buttonText.color
//                opacity: background.opacity
//
//                anchors {
//                    verticalCenter: parent.verticalCenter
//                }
//            }
        }
    }

    DS3.MouseArea {
        onPressed: mouse.accepted = false
    }
}
