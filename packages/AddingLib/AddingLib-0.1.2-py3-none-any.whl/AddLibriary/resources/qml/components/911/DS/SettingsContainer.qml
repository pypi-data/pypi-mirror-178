import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS" as DS

//  Example usage:
//  ...
//  DS.SettingsContainer {
//      Component1 {}
//      Component2 {}
//  }
//  ...


Item {
//  Color of the container's corners
    property alias cornerColor: corners.color

//  Data that should be placed inside the column
    default property alias data: content.data

    implicitWidth: 300
    implicitHeight: content.height

    Column {
        id: content

        width: parent.width
    }

    Rectangle {
        id: corners
        anchors.fill: content
        color: ui.backgrounds.base
        visible: false

        Rectangle {
            height: 16
            width: parent.width

            anchors.bottom: parent.bottom

            radius: 12
            color: ui.backgrounds.lowest
        }
    }

    Item {
        id: mask

        anchors.fill: content

        visible: false

        Rectangle {
            id: maskCorners

            anchors {
                fill: parent
                bottomMargin: 1
            }

            radius: 12
        }
    }

    OpacityMask {
        anchors.fill: corners
        source: corners
        maskSource: mask
        invert: true
    }
}
