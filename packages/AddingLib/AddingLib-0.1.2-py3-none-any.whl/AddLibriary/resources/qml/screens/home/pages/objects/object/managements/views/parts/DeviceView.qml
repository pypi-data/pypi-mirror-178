import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/" as Custom


ScrollView {
    id: topLevel

    height: deviceLoader.height
    width: deviceLoader.width
    opacity: (hub && device && device.online && hub.online) ? 1 : 0.3
    contentHeight: column.height

    contentWidth: -1

    clip: true

    /*
    property alias viewControl: control

    ScrollBar.vertical: Custom.ScrollBar {
        id: control
        parent: topLevel

        anchors {
            top: parent.top
            right: parent.right
            bottom: parent.bottom
        }
    }
    */
//    ScrollBar.horizontal: Custom.ScrollBar { visible: false }
}
