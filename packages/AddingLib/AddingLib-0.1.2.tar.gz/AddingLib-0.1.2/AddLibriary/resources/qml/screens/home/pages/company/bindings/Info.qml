import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    clip: true
    color: ui.colors.dark3
    visible: !!currentObject

    Layout.alignment: Qt.AlignTop | Qt.AlignRight
    Layout.fillHeight: true
    Layout.minimumWidth: 330
    Layout.maximumWidth: 330
    Layout.rightMargin: 8

    property var currentObject: null

    function updateSource() {
        if (!currentObject) {
            bindingsLoader.setSource("")
            return
        }

        var path = "qrc:/resources/qml/screens/home/pages/company/bindings/StaticInfoComponent.qml"
        bindingsLoader.setSource(path)
    }

    onCurrentObjectChanged: {
        updateSource()
    }

    Loader {
        id: bindingsLoader
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
    }
}
