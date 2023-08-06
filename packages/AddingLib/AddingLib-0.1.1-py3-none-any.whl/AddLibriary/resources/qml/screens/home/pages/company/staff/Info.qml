import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    clip: true
    color: ui.colors.dark3
    visible: currentObject
    property var editMode: false
    property var currentObject: null

    Layout.alignment: Qt.AlignTop | Qt.AlignRight
    Layout.fillHeight: true
    Layout.minimumWidth: 330
    Layout.maximumWidth: 330
    Layout.rightMargin: 8

    function updateSource() {
        var path = "qrc:/resources/qml/screens/home/pages/company/staff/"
        path = editMode ? "EditInfoComponent.qml" : "StaticInfoComponent.qml"
        staffLoader.setSource(path)
    }

    onCurrentObjectChanged: {
        editMode = false
        updateSource()
    }

    onEditModeChanged: {
        updateSource()
    }

    Loader {
        id: staffLoader
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
    }
}