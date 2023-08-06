import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Controls.impl 2.2
import QtQuick.Templates 2.2 as T

import "qrc:/resources/qml/components/911/" as Custom

Item {
    id: topLevel
    property var placeHolderText: ""
    property alias control: control
    property var valid: true
    property var error: ""
    property var color: ui.colors.dark1
    property var preferredHeight: 136
    property var maximumLength: 0
    property var value: ""
    height: background.height + (error ? errorText.contentHeight + 6: 0)

    Rectangle {
        id: background
        color: topLevel.color
        width: control.width
        height: {
            if (control.contentHeight < topLevel.preferredHeight) return topLevel.preferredHeight
            return control.contentHeight + 24
        }
        radius: (control.activeFocus || !valid) ? 8 : 10
        border.width: (control.activeFocus || !valid) ? 1 : 0
        border.color: valid ? ui.colors.green3 : ui.colors.red3
    }

    TextArea {
        id: control
        selectByMouse: true
        color: ui.colors.white
        font.pixelSize: 14
        font.family: roboto.name
        opacity: enabled ? 1.0 : 0.5
        horizontalAlignment: TextInput.AlignLeft
        width: parent.width
        anchors.centerIn: parent
        leftPadding: 12
        selectionColor: ui.colors.green1
        selectedTextColor: ui.colors.dark4
        rightPadding: 12

        onActiveFocusChanged: {
            if (!valid) {
                valid = true
                error = ""
            }
        }

        Keys.onPressed: {
            if (maximumLength != 0 && control.text.length <= maximumLength)
                value = control.text
        }

        onTextChanged: {
            if (maximumLength != 0 && control.text.length > maximumLength)
                control.text = value

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
        anchors.topMargin: 6
        color: ui.colors.red1
        font.pixelSize: 12
        wrapMode: Text.WordWrap
        textFormat: Text.PlainText
    }
}
