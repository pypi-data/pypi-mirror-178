
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12
import QtQuick.Layouts 1.3


Item {
    height: 64

    Image {
        id: additionalImage
        visible: false
        source: {
            if (!group) return ""
            return group.small_image_link == "WRONG" ? "qrc:/resources/images/desktop/delegates/RoomPicture/RoomPictureMedium.png" : group.small_image_link
        }
        onStatusChanged: {
            if (status == Image.Error || status == Image.Null || status == Image.Loading) {
                image.source = "qrc:/resources/images/desktop/delegates/RoomPicture/RoomPictureMedium.png"
            } else {
                image.source = group.small_image_link == "WRONG" ? "qrc:/resources/images/desktop/delegates/RoomPicture/RoomPictureMedium.png" : group.small_image_link
            }
        }
    }

    Image {
        id: image
        visible: false
        width: 52
        height: 52
        source: {
            if (!group) return ""
            return group.small_image_link == "WRONG" ? "qrc:/resources/images/desktop/delegates/RoomPicture/RoomPictureMedium.png" : group.small_image_link
        }
        anchors {
            left: parent.left
            leftMargin: 22
            verticalCenter: parent.verticalCenter
        }
    }

    OpacityMask {
        anchors.fill: image
        source: image

        maskSource: Rectangle {
            width: 52
            height: 52
            radius: width / 2
            visible: false
        }
    }

    Text {
        id: groupNameLabel
        text: !!group ? group.name : ""
        color: ui.colors.light1
        font.family: roboto.name
        font.pixelSize: 14
        width: parent.width - 200
        elide: Text.ElideRight
        anchors {
            left: image.right
            leftMargin: 16
            top: parent.top
            topMargin: 2
        }
    }

    Text {
        id: groupIdLabel
        text: "ID " + (!!group ? group.group_id_dec : "")
        color: ui.colors.white
        opacity: 0.6
        font.family: roboto.name
        font.pixelSize: 12
        font.weight: Font.Light
        anchors {
            left: image.right
            leftMargin: 16
            top: groupNameLabel.bottom
        }
    }

    RowLayout {
        spacing: 0

        anchors {
            left: image.right
            leftMargin: 16
            bottom: parent.bottom
            bottomMargin: 5
        }

        Rectangle {
            width: noDevicesLabel.contentWidth + 6
            height: 14
            color: "#f64347"
            radius: 3
            visible: !counts.visible

            Text {
                id: noDevicesLabel
                text: tr.no_devices_lable
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 10
                font.weight: Font.Light
                anchors.centerIn: parent
            }
        }

        Item {
            id: counts
            width: devicesLabel.contentWidth
            height: 14
            visible: !!group && group.devices_count

            Text {
                id: devicesLabel
                text: tr.devices_count_desktop + ": " + (!!group ? group.devices_count : "")
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 11
                font.weight: Font.Light
                font.capitalization: Font.Capitalize
                anchors.centerIn: parent
            }
        }
    }
}
