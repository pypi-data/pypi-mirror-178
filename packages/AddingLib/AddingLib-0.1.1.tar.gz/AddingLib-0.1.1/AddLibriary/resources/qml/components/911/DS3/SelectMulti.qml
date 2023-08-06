import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
//  Whether checked or not
    property bool checked: false

    width: 24
    height: 24

    border {
        width: checked ? 0 : 1
        color: ui.ds3.figure.secondary
    }
    color: checked ? ui.ds3.figure.interactive : ui.ds3.figure.transparent
    radius: 12

    DS3.Icon {
        anchors.centerIn: parent

        visible: checked
        source: "qrc:/resources/images/Athena/common_icons/checkMark.svg"
        color: ui.ds3.figure.inverted
    }
}
