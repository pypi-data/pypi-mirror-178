import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Controls.impl 2.2
import QtQuick.Templates 2.2 as T

Rectangle {
    id: topLevel
    signal searchStarted(variant data)
    signal reload()
    property var placeHolderText: tr.a911_search
    property alias control: control
    property alias ico: ico
    property var valid: true
    property var clearing: true
    property var action: null

    color: ui.colors.dark1
    height: 42
    radius: control.activeFocus ? 0 : 10
    border.width: !control.activeFocus ? 0 : 1
    border.color: valid ? ui.colors.green3 : ui.colors.green3

    Timer {
        id: searchTimer
        interval: 200
        running: false
        property var previousText: ""
        onTriggered: {
            if (previousText == control.text.trim()) return
            searchStarted(control.text.trim())
            previousText = control.text.trim()
        }
    }

    TextField {
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
        rightPadding: 38

        onTextChanged: {
            searchTimer.stop()
            searchTimer.start()
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

    Image {
        id: ico
        width: 28
        height: 28
        source: {
            if (!topLevel.clearing) return "qrc:/resources/images/icons/ic-search.png"
            return control.text == "" ? "qrc:/resources/images/icons/ic-search.png" : "qrc:/resources/images/icons/ic-clear.png"
        }
        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 6
        }

        HandMouseArea {
            enabled: !topLevel.clearing || control.text != ""
            onClicked: {
                if (topLevel.clearing) {
                    control.text = ""
                    reload()
                    return
                }

                if (topLevel.action) {
                    topLevel.action()
                }
            }
        }
    }
}
