import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS" as DS


Rectangle {
    id: groupSwitch

//  Image of the group
    property alias image: image.source
//  Weather switch is ON
    property alias checked: control.checked
//  Title text
    property alias title: titleItem.text
//  Subtitle text
    property alias subTitle: subTitleItem.text
//  Info text
    property alias info: infoItem.text
//  Callback on switch toggled. Default is auto toggle
    property var onToggle: () => {
        checked = !checked
    }

    implicitWidth: parent.width
    implicitHeight: 80

    opacity: enabled ? 1 : 0.3
    color: ui.backgrounds.high

    DS.Image {
        id: defaultImage

        anchors.fill: image

        source: "qrc:/resources/images/Athena/common_icons/groupDefault.svg"
        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
        visible: image.status != Image.Ready
    }

    DS.Image {
        id: image

        width: 64
        height: 64

        anchors {
            left: parent.left
            leftMargin: 24
            verticalCenter: parent.verticalCenter
        }

        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
    }

    Rectangle {
        id: circle

        anchors.fill: image

        radius: width / 2
        visible: false
    }

    Column {
        anchors {
            left: image.right
            right: control.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        DS.TextBodyMBold {
            id: titleItem

            elide: Text.ElideRight
        }

        DS.TextBodySRegular {
            id: subTitleItem

            color: ui.colors.secondary
            elide: Text.ElideRight
        }

        DS.Spacing {
            height: 6
        }

        DS.TextBodySRegular {
            id: infoItem

            elide: Text.ElideRight
        }
    }

    DS.Switch {
        id: control

        anchors {
            right: parent.right
            rightMargin: 24
            verticalCenter: parent.verticalCenter
        }

        z: 1

        onToggled: onToggle()
    }

    Rectangle {
        width: 4
        height: parent.height

        anchors.left: parent.left

        color: ui.colors.interactive
        visible: area.containsMouse || control.containsMouse
    }

    Rectangle {
        width: parent.width
        height: 1

        anchors.bottom: parent.bottom

        color: ui.backgrounds.lowest
    }

    DS.MouseArea {
        id: area

        z: 0
        propagateComposedEvents: true
        cursorShape: Qt.ArrowCursor
    }
}
