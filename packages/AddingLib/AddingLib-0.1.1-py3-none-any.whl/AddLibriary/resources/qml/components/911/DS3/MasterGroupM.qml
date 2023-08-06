import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
//  Image of the group
    property alias image: image
//  Title text
    property alias atomTitle: atomTitle
//  Description text
    property alias descText: descText
//  the text column for setting the right anchors and sizes
    property alias textColumn: textColumn
//  athena status
    property var status: ui.ds3.status.DEFAULT
//  color defined based on the status
    readonly property var statusColor: ({
        [ui.ds3.status.DEFAULT]: ui.ds3.figure.base,
        [ui.ds3.status.WARNING]: ui.ds3.figure.warningContrast,
    })[status]

    implicitWidth: parent.width
    implicitHeight: Math.max(image.height + 24, textColumn.height + 16)

    color: ui.ds3.figure.transparent

    DS3.Image {
        id: defaultImage

        width: 40
        height: 40

        anchors {
            top: parent.top
            topMargin: 12
            left: parent.left
            leftMargin: 16
        }

        source: "qrc:/resources/images/Athena/common_icons/Groups-L.svg"
        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
        opacity: enabled ? 1 : 0.3
        visible: image.status != Image.Ready
    }

    DS3.Image {
        id: image

        width: 40
        height: 40

        anchors {
            top: parent.top
            topMargin: 12
            left: parent.left
            leftMargin: 16
        }

        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
        opacity: enabled ? 1 : 0.3
    }

    Rectangle {
        id: circle

        anchors.fill: image

        radius: width / 2
        visible: false
    }

    Column {
        id: textColumn

        anchors {
            left: image.right
            leftMargin: 16
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        opacity: enabled ? 1 : 0.3

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width

            titleItem.wrapMode: Text.WordWrap
            isBold: true
        }

        DS3.Spacing {
            height: descText.visible ? 4 : 0
        }

        DS3.Text {
            id: descText

            width: parent.width

            style: ui.ds3.text.body.SRegular
            color: statusColor
            visible: !!descText.text
        }
    }
}
