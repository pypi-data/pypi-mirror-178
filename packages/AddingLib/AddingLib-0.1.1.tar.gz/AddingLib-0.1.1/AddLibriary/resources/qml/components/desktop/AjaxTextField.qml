import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Controls.impl 2.2
import QtQuick.Templates 2.2 as T

TextField {
    id: topLevel
    text: ""
    property var placeHolderText: ""
    selectByMouse: true
    color: ui.colors.light1
    font.pixelSize: 12
    font.family: roboto.name
    leftPadding: 2
    bottomPadding: 5
    property bool valid: true
    opacity: enabled ? 1.0 : 0.5
    horizontalAlignment: TextInput.AlignLeft
    property bool allowChanges: false
    selectionColor: ui.colors.green1

    onTextChanged: {
        if (allowChanges) return
        text = text
    }

    onActiveFocusChanged: {
        if (!valid) {
            valid = true
        }
    }

    PlaceholderText {
        id: placeholder
        x: topLevel.leftPadding
        y: topLevel.topPadding
        width: topLevel.width - (topLevel.leftPadding + topLevel.rightPadding)
        height: topLevel.height - (topLevel.topPadding + topLevel.bottomPadding)

        text: topLevel.placeHolderText
        font: topLevel.font
        opacity: 0.4
        color: ui.colors.light1
        verticalAlignment: topLevel.verticalAlignment
        visible: !topLevel.length && !topLevel.preeditText && (!topLevel.activeFocus || topLevel.horizontalAlignment !== Qt.AlignHCenter)
        elide: Text.ElideRight
    }

    background: Item {
        Rectangle {
            id: bottomBorder
            width: parent.width
            height: 1
            color: {
                if (!topLevel.valid) return "#e2252b"
                if (topLevel.readOnly) return "#4e4e4e"
                return topLevel.focus ? "#60e3ab" : "#4e4e4e"
            }
            opacity: 0.8
            anchors.top: parent.bottom

            Behavior on color {
                ColorAnimation { duration: 200 }
            }
        }
    }
}