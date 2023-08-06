import QtQuick 2.12
import QtQuick.Controls 2.13

Item {
    property var visibleIcon: false
    width: 40
    height: 40
    Image {
        source: "qrc:/resources/images/icons/a-plus-button.svg"
        sourceSize.width: 32
        sourceSize.height: 32
        anchors.centerIn: parent
//        rotation: -45
    }
}