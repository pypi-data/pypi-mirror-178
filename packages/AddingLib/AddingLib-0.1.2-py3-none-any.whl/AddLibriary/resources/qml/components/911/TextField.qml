import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Controls.impl 2.2
import QtQuick.Templates 2.2 as T

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: topLevel
    property var placeHolderText: ""
    property alias control: control
    property var color: ui.colors.dark1
    property var valid: true
    property var error: ""
    property var errorColor: ui.colors.red3
    property alias errorText: errorText
    height: background.height + (error ? errorText.contentHeight + 6: 0)

    property alias background: background

    property var errorMargin: 6
    property var errorPixelSize: 12
    property var errorTextColor: ui.colors.red2


    Rectangle {
        id: background
        color: topLevel.color
        height: control.contentHeight + 24
        width: control.width
        radius: (control.activeFocus || !valid) ? 8 : 10
        border.width: (control.activeFocus || !valid) ? 1 : 0
        border.color: valid ? ui.colors.green3 : topLevel.errorColor
        anchors.centerIn: control
    }


    TextField {
        id: control
        selectByMouse: true
        color: ui.colors.white
        font.pixelSize: 14
        font.family: roboto.name
        opacity: enabled ? 1.0 : 0.5
        width: parent.width
        height: 32
        leftPadding: 12
        selectionColor: ui.colors.green1
        selectedTextColor: ui.colors.dark4
        rightPadding: 12
        maximumLength: 300

        onActiveFocusChanged: {
            if (!valid) {
                valid = true
                error = ""
            }
        }

        onTextChanged: {
            if (!valid) {
                valid = true
                error = ""
            }
        }

        PlaceholderText {
            id: placeholder
            x: control.leftPadding
            y: control.topPadding
            width: control.width - (control.leftPadding + control.rightPadding)
            height: control.height - (control.topPadding + control.bottomPadding)

            text: topLevel.placeHolderText
            font: control.font
            opacity: 0.3
            color: ui.colors.white
            verticalAlignment: control.verticalAlignment
            visible: !control.length && !control.preeditText && (!control.activeFocus || control.horizontalAlignment !== Qt.AlignHCenter)
            elide: Text.ElideRight
        }

        background: Item {}
    }

    Custom.FontText {
        id: errorText
        width: parent.width
        text: error
        anchors.top: control.bottom
        anchors.topMargin: topLevel.errorMargin
        color: topLevel.errorTextColor
        font.pixelSize: topLevel.errorPixelSize
        wrapMode: Text.WordWrap
        textFormat: Text.PlainText
    }
}
