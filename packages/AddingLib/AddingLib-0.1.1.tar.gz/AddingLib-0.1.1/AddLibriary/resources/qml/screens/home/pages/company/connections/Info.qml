import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    clip: true
    color: ui.colors.dark4
    visible: currentObject
    property var currentObject: null
    property alias connectionsLoader: connectionsLoader

    Layout.alignment: Qt.AlignTop | Qt.AlignRight
    Layout.fillHeight: true
    Layout.minimumWidth: 330
    Layout.maximumWidth: 330
    Layout.rightMargin: 8

    function updateSource() {
        var path = "qrc:/resources/qml/screens/home/pages/company/connections/"
        path = "StaticInfoComponent.qml"
        connectionsLoader.setSource(path)
    }

    onCurrentObjectChanged: {
        updateSource()
    }

    Loader {
        id: connectionsLoader
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
    }
}