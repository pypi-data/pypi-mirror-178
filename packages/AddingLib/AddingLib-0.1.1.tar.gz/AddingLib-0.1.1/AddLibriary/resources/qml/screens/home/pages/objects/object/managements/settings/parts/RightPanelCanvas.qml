import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

Rectangle {
    width: 360
    height: parent.height

    property alias testLoader: testLoader

    anchors.right: parent.right
    visible: popup.width != 360
    color: ui.backgrounds.base
    radius: 12

    Loader {
        id: testLoader
        anchors.fill: parent
    }
}