import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


// Regular button
Button {
    id: buttonContained

//  If button is red
    property bool isAttention
//  the view of button (if outline, then background is transparent)
    property var isOutline
//  does the button icon on the left
    property bool isIconLeft: true
//  maximum width of the button
    property var maxWidth
//  source of the icon
    property var buttonIconSource: ""
//  if button with border
    property bool hasBorder: true
//  if icon has animation
    property alias animIcon: icon
//  If something loading
    property bool isLoadState
    /* -------------------------------------------- */
    /* desktop tests */
    property var accessibleAreaName: ""
    /* -------------------------------------------- */

    width: -1
    height: 48

    Component.onCompleted: {
        if (width == -1) {
            buttonContained.width = Qt.binding(() => content.width + 32)
            buttonText.width = Qt.binding(
                () => Math.min(
                    buttonContained.maxWidth - (icon.visible ? (icon.width + content.spacing) : 0) - 32,
                    fakeText.width
                )
            )
        } else {
            buttonText.width = Qt.binding(() => {
                const iconWidth = (icon.visible ? (icon.width + content.spacing) : 0)
                if (fakeText.width + iconWidth + 32 > buttonContained.width) {
                    return buttonContained.width - iconWidth - 32
                }
                return fakeText.width
            })
        }
    }

    background: Rectangle {
        anchors.fill: parent

        radius: height
        color: {
            if (isLoadState || isOutline) return ui.ds3.figure.transparent
            return isAttention ? ui.ds3.figure.attention : ui.ds3.figure.interactive
        }
        opacity: !enabled ? 0.3 : (pressed ? 0.6 : 1)
        border.color: {
            if (isLoadState || !hasBorder) return ui.ds3.figure.transparent
            return isAttention ? ui.ds3.figure.attention : ui.ds3.figure.interactive
        }
    }

    contentItem: Item {
        Row {
            id: content

            height: parent.height

            anchors {
                horizontalCenter: parent.horizontalCenter
                verticalCenter: parent.verticalCenter
            }

            spacing: 5
            layoutDirection: isIconLeft ? Qt.LeftToRight : Qt.RightToLeft

            DS3.Icon {
                id: icon

                anchors.verticalCenter: parent.verticalCenter

                visible: !!source.toString() && !isLoadState
                source: buttonIconSource
                color: buttonText.color
                opacity: background.opacity
            }

            DS3.Spinner {
                anchors.verticalCenter: parent.verticalCenter

                size: DS3.Spinner.ImageSize.S
                visible: isLoadState
            }

            DS3.Text {
                id: buttonText

                anchors.verticalCenter: parent.verticalCenter

                text: buttonContained.text
                style: ui.ds3.text.body.MBold
                font.letterSpacing: 0.7
                color: {
                    if (isLoadState) return ui.ds3.figure.secondary
                    if (!isOutline) return ui.ds3.figure.inverted
                    return isAttention ? ui.ds3.figure.attention : ui.ds3.figure.interactive
                }
                opacity: background.opacity
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                hasElide: true
            }
        }

        DS3.Text {
            // fake component to determine text width
            id: fakeText

            text: buttonContained.text
            style: ui.ds3.text.body.MBold
            font.letterSpacing: 0.7
            visible: false
        }
    }

    DS3.MouseArea {
        onPressed: mouse.accepted = false
    }

    /* -------------------------------------------- */
    /* desktop tests */
    Accessible.name: buttonContained.accessibleAreaName
    Accessible.description: "<button enabled=" + Accessible.checkable + ">" + buttonContained.text + "</button>"
    Accessible.role: Accessible.Button
    Accessible.checkable: visible && enabled
    Accessible.onPressAction: {
        if (!Accessible.checkable) return
        buttonContained.clicked(true)
    }
    /* -------------------------------------------- */
}