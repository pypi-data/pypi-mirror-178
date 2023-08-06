import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


Button {
    id: control

    property var color: ui.colors.green1
    property var transparent: false
    property var loading: false
    property var loading_background_color: ui.colors.dark1
    property var enabledCustom: true
    property var radius: 224
    property var animColor: ui.colors.green1
    enabled: {
        if (loading) return false
        return enabledCustom
    }
    property alias textButton: textButton

    property alias anim: anim
    property alias backgroundItem: backgroundItem
    property alias mouseArea: mouseArea

    focusPolicy: Qt.NoFocus

    contentItem: Item {
        FontText {
            id: textButton
            text: control.text
            color: {
                if (!enabled) return ui.colors.middle3
                return transparent ? control.color : ui.colors.black
            }
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.fill: parent
            visible: !loading
        }
    }

    background: Rectangle {
        id: backgroundItem
        color: {
            if (loading) return "transparent"
            if (!enabled) return ui.colors.middle4
            return control.transparent ? "transparent" : control.color
        }
        width: {
            return control.down ? control.width - 4 : control.width
        }
        implicitHeight: control.down ? 38 : 42
        opacity: {
            if (loading) return 1
            return enabled ? 1 : 0.3
        }
        border.color: {
            if (loading) return "transparent"
            if (!enabled) return "transparent"
            return control.color
        }
        border.width: 1
        radius: control.radius
        anchors.centerIn: parent

        Rectangle {
            visible: loading
            width: 48
            height: 48
            radius: 12
            color: loading_background_color
            anchors.centerIn: parent
            anchors.verticalCenterOffset: -4

            Anime.SharinganLoader {
                id: anim
                radius: 13
                color: control.animColor
                useCircle: true
                anchors.centerIn: parent
                anchors.verticalCenterOffset: -4
            }
        }
    }

    Custom.HandMouseArea {
        id: mouseArea

        anchors.fill: parent
        onPressed: {
            mouse.accepted = false
        }
    }
}