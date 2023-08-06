import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: deviceCardNavigation

//  Component atomTitle
    property alias atomTitle: atomTitle
//  The status text
    property alias statusText: status.text
//  Image source
    property alias imageSource: image.source
//  The badge counter text
    property alias badgeCounter: badge.text
//  Is this card highlighted
    property bool highlighted: area.containsMouse
//  Is the device online
    property bool isOnline: false
//  Is this card selected
    property bool selected: false

// On card clicked
    signal clicked()

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleBadgeName: ""
    property var accessibleImageName: ""
    property var accessibleStatusName: ""
    /* ---------------------------------------------------- */

    width: parent.width
    height: 80

    color: {
        if (selected) return ui.ds3.special.selection
        if (isOnline) return (highlighted ? ui.ds3.bg.high : ui.ds3.bg.highest)
        return ui.ds3.bg.base
    }
    radius: 12
    border {
        width: isOnline || selected ? 0 : 2
        color: highlighted ? ui.ds3.bg.high : ui.ds3.bg.highest
    }

    DS3.BadgeAttention {
        id: badge

        anchors {
            left: parent.left
            top: parent.top
            topMargin: 12
        }

        visible: !!text && text > 0

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: deviceCardNavigation.accessibleBadgeName
        Accessible.description: deviceCardNavigation.badgeCounter
        Accessible.role: Accessible.Paragraph
        /* ---------------------------------------------------- */
    }

    DS3.Image {
        id: image

        width: 40
        height: 40

        anchors {
            left: parent.left
            top: parent.top
            leftMargin: 16
            topMargin: 12
        }

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: accessibleImageName
        Accessible.description: source
        Accessible.role: Accessible.Graphic
        /* ---------------------------------------------------- */
    }

    Column {
        anchors {
            left: image.right
            top: parent.top
            right: parent.right
            leftMargin: 16
            rightMargin: 16
            topMargin: 8
        }

        spacing: 4

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width

            elide: Text.ElideRight
        }

        DS3.Text {
            id: status

            width: parent.width

            color: ui.ds3.figure.attention
            style: ui.ds3.text.body.SRegular

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: deviceCardNavigation.accessibleStatusName
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }
    }

    DS3.MouseArea {
        id: area

        onClicked: deviceCardNavigation.clicked()
    }
}
