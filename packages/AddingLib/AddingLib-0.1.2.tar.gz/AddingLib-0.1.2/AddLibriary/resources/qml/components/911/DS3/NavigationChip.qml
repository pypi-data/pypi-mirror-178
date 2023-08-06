import QtQuick 2.12
import QtQuick.Controls 2.13

import 'qrc:/resources/qml/components/911/DS3' as DS3


Rectangle {
    id: tabItem
    
//  Whether chip is selected
    property bool selected
//  Text of the chip
    property alias label: label.text

    signal clicked
    
    width: label.width + 24
    height: 32

    radius: 16
    color: selected ? ui.ds3.bg.lowest : ui.ds3.bg.low

    DS3.Text {
        id: label

        anchors.centerIn: parent

        style: ui.ds3.text.body.MBold
        color: selected ? ui.ds3.figure.base : ui.ds3.figure.nonessential
    }

    DS3.MouseArea {
        id: typeArea

        onClicked: {
            tabItem.clicked()
        }
    }
}
