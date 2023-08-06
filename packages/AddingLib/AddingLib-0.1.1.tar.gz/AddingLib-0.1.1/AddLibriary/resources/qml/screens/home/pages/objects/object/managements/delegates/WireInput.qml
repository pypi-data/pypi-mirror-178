import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/delegates/parts"
import "qrc:/resources/qml/components/911/DS3/" as DS3

Item {
    id: delegate

    property var imageSource: Images.get_image(device.input_is_tamper == 1 ? "26-wired-tamper" : "26-wired-intrusion", "Medium")

    property alias flow: flow
    property alias image: deviceImage

    opacity: (!device || !hub || !device.online || !hub.online) ? 0.3 : 1

    Item {
        id: deviceImage

        width: 72
        height: 72

        anchors {
            left: parent.left
            leftMargin: 8
        }

        Image {
            width: 72
            height: 72

            source: delegate.imageSource

            /* ------------------------------------------------ */
            /* desktop tests */
            Accessible.name: {
                if (!delegate.parent.parent.accessiblePrefix) return ""
                return __accessible_unique_ids__ ? delegate.parent.parent.accessiblePrefix + "_image" : "image"
            }
            Accessible.description: source
            Accessible.role: Accessible.Graphic
            /* ------------------------------------------------ */
        }

        Column {
            width: delegate.width - (deviceDelegate.settingsVisible ? 144 : 88)

            anchors {
                top: parent.top
                topMargin: 8
                left: deviceImage.right
                leftMargin: 12
                verticalCenter: parent.verticalCenter
            }

            spacing: 2

            Custom.FontText {
                id: deviceName

                width: parent.width

                anchors.left: parent.left

                text: device.name
                color: ui.colors.light1
                textFormat: Text.AutoText
                elide: Text.ElideRight

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: {
                    if (!delegate.parent.parent.accessiblePrefix) return ""
                    return __accessible_unique_ids__ ? delegate.parent.parent.accessiblePrefix + "_name" : "name"
                }
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ------------------------------------------------ */
            }

            Custom.FontText {
                id: roomName

                width: parent.width

                anchors.left: parent.left

                visible: currentTab !== "ROOMS"
                text: device.room_name
                color: ui.colors.light1
                textFormat: Text.AutoText
                font.pixelSize: 12
                opacity: 0.4
                elide: Text.ElideRight
            }
        }
    }

    DS3.BadgeAttention {
        id: issues

        visible: device.issue_count > 0
        text: device.issue_count
    }

    Flow {
        id: flow

        width: parent.width - 104
        height: childrenRect.height

        anchors {
            left: deviceImage.right
            leftMargin: 12
            bottom: parent.bottom
            bottomMargin: 8
        }

        spacing: 8
        opacity: !device.online ? 0.4 : 1

        FlowIco {}
    }
}
