import QtQuick 2.12
import QtQuick.Controls 2.13


Item {
    id: newPhoneNumberItem

    property alias newPhoneNumber: newPhoneNumber

    anchors {
        top: passwordItem.bottom
        topMargin: 24
        horizontalCenter: parent.horizontalCenter
    }

    TextFieldEdit {
        id: newPhoneNumber

        width: parent.width

        distance: 20
        key: tr.new_phone_number
        value: ""
        valueText.control {
            font.pixelSize: 16
            color: ui.colors.light3
            maximumLength: 30
            validator: RegExpValidator { regExp: /\+?[0-9]+/ }

            onTextEdited: {
                var t = valueText.control.text
                if (!t.startsWith("+")) valueText.control.text = "+" + t
            }
        }

        Connections {
            target: newPhoneNumber.valueText.control

            function onActiveFocusChanged(focus) {
                tooltip.visible = focus
                var t = target.text
                if (focus) {
                    target.text = t == "" ? "+" : t
                } else {
                    target.text = t == "+" ? "" : t
                }
            }
        }
    }

    Item {
        id: tooltipItem

        width: newPhoneNumberItem.width

        anchors {
            top: newPhoneNumberItem.bottom
            topMargin: 28
            horizontalCenter: parent.horizontalCenter
        }

        ToolTip {
            id: tooltip
            parent: parent

            contentItem: Text {
                text: tr.phone_tip
                font.family: roboto.name
                font.pixelSize: 12
                color: ui.colors.light1
            }

            background: Rectangle {
                color: ui.colors.dark4
                radius: 4
                border {
                    width: 1
                    color: ui.colors.green1
                }
            }
        }
    }
}
