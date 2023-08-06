import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Item {
    width: 26
    height: 24
    visible: !(deviceLoader.source == "")
    z: 100
    Image {
        sourceSize.width: 24
        sourceSize.height: 24
        anchors.centerIn: parent
        source: "qrc:/resources/images/icons/back.svg"
    }
    Custom.HandMouseArea {
        onClicked: {
            deviceLoader.source = ""
        }
    }
}
