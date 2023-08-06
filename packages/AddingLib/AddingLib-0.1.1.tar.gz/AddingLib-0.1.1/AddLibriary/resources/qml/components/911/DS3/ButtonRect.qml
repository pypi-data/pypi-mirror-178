import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


// Rect button
Button {
    id: buttonRect

// Enum that has all the status types to show the appropriate color for text in button
    enum Status {
        Default,        // default
        Attention,
        Secondary
    }
//  color of button background
    property var color: ui.ds3.bg.highest
//  does the button icon on the left
    property var isIconLeft: true
//  maximum width of the button
    property var maxWidth
//  source of the icon
    property var buttonIconSource: ""
//  status value that accepts the status (should be in the Status enum)
    property var status: DS3.ButtonRect.Status.Default
//  the mapping of status to color
    readonly property var colorStatus: {
        switch (status) {
            case DS3.ButtonRect.Status.Default: return ui.ds3.figure.interactive
            case DS3.ButtonRect.Status.Secondary: return ui.ds3.figure.secondary
            case DS3.ButtonRect.Status.Attention: return ui.ds3.figure.attention
        }
    }
//  opacity for text and icon
    property var generalOpacity: 1
//  if icon has animation
    property alias animIcon: icon
//  If you need to change button text component
    property alias buttonText: buttonText
//  alias to badge
    property alias badge: badge

    width: 0
    height: 36

    Component.onCompleted: {
        if (!width) {
            buttonRect.width = Qt.binding(() => content.width + 32)
            buttonText.width = Qt.binding(
                () => Math.min(
                    buttonRect.maxWidth - (icon.visible ? (icon.width + content.spacing) : 0) - 32,
                    fakeText.width
                )
            )
        } else {
            buttonText.width = Qt.binding(() => {
                const iconWidth = (icon.visible ? (icon.width + content.spacing) : 0)
                if (fakeText.width + iconWidth + 32 > buttonRect.width) {
                    return buttonRect.width - iconWidth - 32
                }
                return fakeText.width
            })
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

                visible: !!source.toString()
                source: buttonIconSource
                color: buttonText.color
                opacity: generalOpacity
            }

            DS3.Text {
                id: buttonText

                anchors.verticalCenter: parent.verticalCenter

                text: buttonRect.text
                style: ui.ds3.text.body.SBold
                font.letterSpacing: 0.7
                color: colorStatus
                opacity: generalOpacity
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                hasElide: true
            }

            DS3.BadgeRegular {
                id: badge

                anchors.verticalCenter: parent.verticalCenter
            }
        }

        DS3.Text {
            // fake component to determine text width
            id: fakeText

            text: buttonRect.text
            style: ui.ds3.text.body.SBold
            font.letterSpacing: 0.7
            visible: false
        }
    }

    DS3.MouseArea {
        onPressed: mouse.accepted = false
    }
}