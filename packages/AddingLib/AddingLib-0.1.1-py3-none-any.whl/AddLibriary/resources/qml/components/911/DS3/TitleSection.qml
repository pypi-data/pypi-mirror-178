import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
//  Main text
    property alias text: textItem.text
//  Reference to textItem
    property alias textItem: textItem
//  If has text button
    property alias hasButton: textButton.visible
//  Button text (use with hasButton)
    property alias buttonText: textButton.text
//  Caps text variant
    property bool isCaps: false
//  Transparent bg
    property bool isBgTransparent: false
//  Forse text to left
    property bool forceTextToLeft: false
//  Whether top corners are rounded
    property bool isTopRounded: false
//  When clicked on button
    property var onButtonClicked: () => {}

    width: parent.width
    height: visible ? textItem.height + 8 : 0

    clip: true

    Rectangle {
        anchors {
            fill: parent
            bottomMargin: isTopRounded ? -12 : 0
        }

        color: isBgTransparent ? ui.ds3.figure.transparent : ui.ds3.bg.high
        radius: isTopRounded ? 12 : 0
    }

    DS3.Text {
        id: textItem

        anchors {
            left: {
                if (forceTextToLeft) {return parent.left}
                return textButton.visible ? parent.left : undefined
            }
            leftMargin: textButton.visible ? 16 : 0
            verticalCenter: parent.verticalCenter
            centerIn: {
                if (forceTextToLeft) {return undefined}
                return textButton.visible ? undefined : parent
            }
        }

        style: isCaps ? ui.ds3.text.special.SectionCaps : ui.ds3.text.body.MRegular
        color: ui.ds3.figure.secondary
        horizontalAlignment: textButton.visible ? Text.AlignLeft : Text.AlignHCenter
    }

    DS3.Text {
        id: textButton

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        style: ui.ds3.text.body.MRegular
        color: ui.ds3.figure.interactive
        horizontalAlignment: Text.AlignRight
        visible: false

        DS3.MouseArea {
            onClicked: {
                onButtonClicked()
            }
        }
    }
}
