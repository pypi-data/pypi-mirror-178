import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/images.js" as Images

DS3.SettingsContainerItem {
//  Component atomTitle
    property alias atomTitle: atomTitle
//  Type of the device (to find appropriate image)
    property var deviceType
//  Color of the device (to find appropriate image)
    property var deviceColor
//  Subtype of the device (to find appropriate image)
    property var deviceSubtype: "NO_SUBTYPE"
//  If image can't be found (use without deviceType and deviceColor)
    property var imageSource: ""
//  If image is small
    property bool smallImage: false
//  If device is disabled but can be selected
    property bool isOnline: true
//  to access device image
    property alias deviceImage: deviceImage
//  description on the bottom
    property alias description: description
//  list of miniIcons
    property var flowIcoModel
//  the text column for setting the right anchors and sizes
    property alias textColumn: textColumn
//  A test value to show the online of a device.
//  Once all the "Device" components will be redesigned there will be no need for it.
    property var hasOnlineTextMessage: false
//  The badge counter text
    property alias badgeCounter: badge.text

    width: undefined
    height: {
        if (smallImage) return Math.max(64, textColumn.height + 24)
        return Math.max( 104 + ( description.lineCount > 1 ? description.lineHeight : 0 )
            + ( hasOnlineTextMessage && !isOnline ? 16 : 0 ), textColumn.height + 24)
    }

    color: ui.ds3.bg.highest

    Item {
        id: mainBody

        width: parent.width
        height: parent.height

        anchors {
            top: parent.top
            left: parent.left
        }
    }

    DS3.BadgeAttention {
        id: badge

        anchors {
            left: parent.left
            top: parent.top
            topMargin: 12
        }

        visible: !!text && text > 0
    }

    DS3.Image {
        id: deviceImage

        sourceSize.width: smallImage ? 40 : width
        sourceSize.height: smallImage ? 40 : height

        anchors {
            top: parent.top
            topMargin: 12
            left: parent.left
            leftMargin: smallImage ? 16 : 8
        }

        source: imageSource && imageSource.length ? imageSource : Images.get_image(deviceType, "Medium", deviceColor, null, deviceSubtype)
        opacity: {
            if (!(isOnline || hasOnlineTextMessage || hasOnlineTextMessage)) return 0.3
            return enabled ? 1 : 0.3
        }
    }

    Column {
        id: textColumn

        width: parent.width

        anchors {
            left: parent.left
            leftMargin: smallImage ? deviceImage.width + 32 : 112
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        spacing: 4
        opacity: {
            if (!isOnline && !hasOnlineTextMessage) return 0.3
            return enabled ? 1 : 0.3
        }

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width

            isBold: true
        }

        DS3.Text {
            text: tr.offline
            visible: !isOnline && hasOnlineTextMessage
            style: ui.ds3.text.body.SRegular
            color: ui.ds3.figure.attention
        }

        Item {
            width: childrenRect.width
            height: !!flowIcoModel ? 16 : 0

            visible: repeater.count > 0 && isOnline

            Row {
                spacing: 8

                Repeater {
                    id: repeater

                    model: flowIcoModel

                    DS3.Icon {
                        id: imageItem

                        source: repeater.model[index].source
                        color: ui.ds3.figure[repeater.model[index].color]
                    }
                }
            }
        }

        DS3.Text {
            id: description

            width: parent.width

            visible: !!text
            color: ui.ds3.figure.secondary
        }
    }
}