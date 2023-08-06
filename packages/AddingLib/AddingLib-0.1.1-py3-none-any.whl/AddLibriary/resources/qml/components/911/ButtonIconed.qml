import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


Button {
    id: control

    height: 40  // to prevent height decreasing occurred on anim

    property var color: ui.colors.green1
    property var transparent: false
    property var loading: false
    property var loading_background_color: ui.colors.dark1
    property var enabledCustom: true
    property var radius: 224
    enabled: {
        if (loading) return false
        return enabledCustom
    }
    property alias textButton: textButton
    property alias iconImage: iconImage
    property alias backgroundItem: backgroundItem

    property alias anim: anim

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleIconName: ""
    property var accessibleIconDescription: ""

    property var accessibleTextName: ""
    property var accessibleTextDescription: ""

    property var accessibleAreaName: ""
    property var accessibleAreaDescription: ""
    /* ---------------------------------------------------- */

    focusPolicy: Qt.NoFocus

    contentItem: Item {

        Image {
            id: iconImage

            width: 24
            height: 24

            sourceSize.width: 24
            sourceSize.height: 24
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: accessibleIconName
            Accessible.description: accessibleIconDescription
            Accessible.role: Accessible.Graphic
            /* ---------------------------------------------------- */
        }

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

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: accessibleTextName
            Accessible.description: accessibleTextDescription
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }
    }

    background: Rectangle {
        id: backgroundItem

        height: control.down ? parent.height - 4 : parent.height
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
                color: ui.colors.green1
                useCircle: true
                anchors.centerIn: parent
                anchors.verticalCenterOffset: -4
            }
        }
    }

    /* ---------------------------------------------------- */
    /* desktop tests */
    Accessible.name: accessibleAreaName
    Accessible.description: "<button enabled=" + Accessible.checkable + ">" + accessibleAreaDescription + "</button>"
    Accessible.role: Accessible.Button
    Accessible.checkable: visible && enabled
    Accessible.onPressAction: {
        if (!Accessible.checkable) return
        control.clicked(true)
    }
    /* ---------------------------------------------------- */

    Custom.HandMouseArea {
        anchors.fill: parent
        onPressed: {
            mouse.accepted = false
        }
    }
}