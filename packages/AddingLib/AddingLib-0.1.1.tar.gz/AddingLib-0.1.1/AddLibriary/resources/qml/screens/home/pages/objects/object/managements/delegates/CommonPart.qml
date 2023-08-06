import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/delegates/parts"
import "qrc:/resources/qml/components/911/DS3/" as DS3

Item {
    id: delegate

    property alias flow: flow
    property var deviceColor: device.obj_type == "44" ? device.panel_color : device.color
    property var imageSource: Images.get_image(device.obj_type, "Medium", deviceColor, "TAMPER_ALARM", device.subtype)
    property var rexDeleg: false
//  Model from flow icons
    property alias flowIconsModel: flowIcons.flowIconsModel

    Item {
        id: deviceImage

        width: 64
        height: 64

        anchors {
            left: parent.left
            leftMargin: 8
            top: parent.top
            topMargin: 4
        }

        opacity: !!device && !!hub && device.online && hub.online ? 1 : 0.3

        Image {
            width: 64
            height: 64

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

        Row {
            anchors {
                top: parent.top
                topMargin: 4
                left: deviceImage.right
                leftMargin: 12
                verticalCenter: parent.verticalCenter
            }

            Column {
                width: delegate.width - (deviceDelegate.settingsVisible ? 144 : 88) - 52

                anchors {
                    top: parent.top
                    verticalCenter: parent.verticalCenter
                }

                DS3.Text {
                    id: deviceName

                    width: parent.width

                    anchors.left: parent.left

                    text: device.name
                    hasElide: true

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

                DS3.Text {
                    id: roomName

                    width: parent.width

                    anchors.left: parent.left

                    visible: currentTab !== "ROOMS"

                    text: device.room_name
                    style: ui.ds3.text.body.SRegular
                    color: ui.ds3.figure.secondary

                    hasElide: true
                }
            }
        }
    }

    DS3.BadgeAttention {
        id: issues

        anchors {
            left: delegate.left
            top: delegate.top
        }

        visible: device.issue_count > 0
        text: device.issue_count
        opacity: !!device && !!hub && device.online && hub.online ? 1 : 0.3
    }


    Flow {
        id: flow

        width: parent.width - 104
        height: childrenRect.height

        anchors {
            left: deviceImage.right
            leftMargin: 12
            top: parent.top
            topMargin: 48
        }

        spacing: 8
        opacity: !!device && !!hub && device.online && hub.online ? 1 : 0.3

        Item {
            width: inputIndex.width
            height: 18

            visible: device.obj_type == "1d"

            Custom.FontText {
                id: inputIndex

                width: contentWidth
                height: contentHeight

                anchors.verticalCenter: parent.verticalCenter

                text: tr.input + ": " + device.input_index
                color: ui.colors.light3
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignLeft
            }
        }

        FlowIco { id: flowIcons }
    }
}