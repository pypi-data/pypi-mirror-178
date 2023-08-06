import QtQuick 2.12
import QtQuick.Controls 2.13

Item {
    property var visibleIcon: false
    property alias img: img
    width: 40
    height: 40
    Image {
        id: img
        source: "qrc:/resources/images/icons/a-minus-button.svg"
        anchors.centerIn: parent
        rotation: -45
    }
}