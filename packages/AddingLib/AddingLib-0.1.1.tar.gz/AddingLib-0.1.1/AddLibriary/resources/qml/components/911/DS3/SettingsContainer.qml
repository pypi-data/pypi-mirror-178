import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

//  Example usage:
//  ...
//  DS3.SettingsContainer {
//      Component1 {}
//      Component2 {}
//  }
//  ...



Column {
    id: settingsContainer

//  Title of the container
    property alias title: titleSection.text

    width: parent.width

    Rectangle {
        id: roundedMask

        width: settingsContainer.width
        height: settingsContainer.height

        layer.enabled: true
        visible: false
        radius: 12
    }

    DS3.TitleSection {
        id: titleSection

        visible: !!text
    }

    spacing: 1
    layer.enabled: true
    layer.samplerName: "maskSource"
    layer.effect: ShaderEffect {
        property var colorSource: roundedMask

        //fragmentShader: util.shaders.round_corners
    }
}