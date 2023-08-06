import QtQuick 2.7
import QtQuick.Controls 2.2


Item {
    id: topLevel
    width: parent.width
    height: textField.height + 24
    opacity: enabled ? 1.0 : 0.5

    property alias value: valueField.text
    property alias text: textField.text
    property alias placeholderText: valueField.placeholderText
    property alias horizontalAlignment: valueField.horizontalAlignment
    property alias validator: valueField.validator

    AjaxTextField {
        anchors.centerIn: parent

        id: valueField
        width: parent.width - 64
        validator: RegExpValidator { regExp: /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/ }

        Text {
            id: textField
            anchors {
                left: parent.left
                leftMargin: 4
                verticalCenter: parent.verticalCenter
            }

            text: topLevel.text
            font.family: roboto.name
            font.pixelSize: 12
            color: ui.colors.light1
            opacity: 0.8
        }
    }
}