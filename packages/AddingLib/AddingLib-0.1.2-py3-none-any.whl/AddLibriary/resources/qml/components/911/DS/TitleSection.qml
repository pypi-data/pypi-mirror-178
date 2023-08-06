import QtQuick 2.12
import "qrc:/resources/qml/components/911/DS" as DS

Item {

    property var text: "TitleSectionText"

    width: parent.width
    height: 30

    anchors.horizontalCenter: parent.horizontalCenter

    DS.TextBodyMBold {
        text: parent.text

        width: parent.width

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
        }
    }
}