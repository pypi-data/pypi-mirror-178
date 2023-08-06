import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts"

DeviceView {
    id: view

    width: deviceLoader.width
    height: deviceLoader.height
    contentHeight: height
    property var device: null
    property var marginView: 64

    Item {
        anchors.fill: parent

        Custom.EmptySpaceLogo {
            size: parent.width / 2
        }
    }
}
