import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
//  Main text
    property alias text: textItem.text
//  Text style
    property alias textStyle: textItem.style

    implicitWidth: textItem.contentWidth
    height: textItem.height + 8

    DS3.Text {
        id: textItem

        width: parent.width

        anchors.centerIn: parent

        style: ui.ds3.text.title.SBold
        horizontalAlignment: Text.AlignHCenter
    }
}
