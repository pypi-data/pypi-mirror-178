import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Item {
    id: topLevel
    property var text: "default"
    property var source: ""
    property var selected: false
    property alias selectArea: selectArea

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleIconName: ""
    property var accessibleIconDescription: ""

    property var accessibleTextName: ""
    property var accessibleTextDescription: ""

    property var accessibleAreaName: ""
    property var accessibleAreaDescription: ""
    /* ---------------------------------------------------- */

    Item {
        id: item
        width: parent.height
        height: parent.height

        Image {
            sourceSize.width: 32
            sourceSize.height: 32
            source: topLevel.source
            anchors.centerIn: parent
            visible: topLevel.source != ""

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: accessibleIconName
            Accessible.description: accessibleIconDescription
            Accessible.role: Accessible.Graphic
            /* ---------------------------------------------------- */
        }

        Rectangle {
            width: 22
            height: width
            radius: height / 2
            color: selected ? ui.colors.green1 : ui.colors.middle1
            opacity: selected ? 1.0 : 0.3
            visible: topLevel.source == ""
            anchors.centerIn: parent
        }
    }

    Custom.FontText {
        text: topLevel.text
        color: ui.colors.light3
        font.pixelSize: 16
        anchors {
            verticalCenter: parent.verticalCenter
            left: item.right
            leftMargin: 12
        }

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: accessibleTextName
        Accessible.description: accessibleTextDescription
        Accessible.role: Accessible.Paragraph
        /* ---------------------------------------------------- */
    }

    Custom.HandMouseArea {
        id: selectArea
        anchors.fill: parent
    }

    /* ---------------------------------------------------- */
    /* desktop tests */
    Accessible.name: accessibleAreaName
    Accessible.description: "<button enabled=" + Accessible.checkable + ">" + accessibleAreaDescription + "</button>"
    Accessible.role: Accessible.Button
    Accessible.checkable: visible && enabled
    Accessible.onPressAction: {
        if (!Accessible.checkable) return
        selectArea.clicked(true)
    }
    /* ---------------------------------------------------- */
}
