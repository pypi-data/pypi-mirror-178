import QtQuick 2.7
import QtQuick.Controls 2.2


Item {
    width: parent.width
    height: control.height + 12
    opacity: enabled ? 1.0 : 0.5

    property string text: ""

    AjaxCheckBox {
        id: control
        text: parent.text
        width: parent.width - 64
        anchors.centerIn: parent
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
    }
}