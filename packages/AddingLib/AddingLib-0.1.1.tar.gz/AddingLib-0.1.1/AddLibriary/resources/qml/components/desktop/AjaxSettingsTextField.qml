import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/desktop/"

Item {
    width: parent.width
    height: field.contentHeight + 24

    opacity: enabled ? 1.0 : 0.5

    property string fieldText: ""
    property string miniText: ""
    property bool valid: true
    property bool readOnly: false
    property alias field: field
    property bool password: false
    property bool changeIcon: false

    AjaxTextField {
        id: field
        width: parent.width - 64
        anchors.centerIn: parent
        text: fieldText
        leftPadding: 5
        valid: parent.valid
        readOnly: parent.readOnly
        echoMode: password ? TextInput.Password : TextInput.Normal

        Text {
            text: miniText
            color: ui.colors.light1
            opacity: 0.5
            font.family: roboto.name
            font.pixelSize: 10
            anchors {
                top: parent.top
                topMargin: -7
                left: parent.left
                leftMargin: 2
            }
        }

        Image {
            id: penIcon
            visible: changeIcon
            source: "qrc:/resources/images/desktop/icons/ic-pen.png"
            width: 16
            height: 16
            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 10
            }
        }
    }

    Component.onCompleted: {
        if (changeIcon) field.rightPadding = 30
    }
}