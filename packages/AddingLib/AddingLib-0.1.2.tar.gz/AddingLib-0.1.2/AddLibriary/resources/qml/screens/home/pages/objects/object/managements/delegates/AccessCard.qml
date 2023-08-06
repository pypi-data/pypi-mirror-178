import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/delegates/parts"

Item {
    id: delegate
    opacity: (!device || !hub || !device.online || !hub.online) ? 0.3 : 1

    property var imageSource: Images.get_image(device.card_type, "Medium", device.color)

    property alias flow: flow
    property alias image: deviceImage

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

            anchors.centerIn: parent

            fillMode: Image.PreserveAspectFit
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

        Item {
            width: 50
            height: 32

            anchors {
                top: parent.top
                topMargin: 2
                left: deviceImage.right
                leftMargin: 12
            }

            Custom.FontText {
                id: deviceName

                width: delegate.width - (deviceDelegate.settingsVisible ? 144 : 88)

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                }

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
        }

        Item {
            width: 50
            height: 32

            anchors {
                bottom: parent.bottom
                bottomMargin: 20
                left: deviceImage.right
                leftMargin: 12
            }

            Custom.FontText {
                id: userName

                width: delegate.width - (deviceDelegate.settingsVisible ? 144 : 88)

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                }

                text: {
                    var user_id = device.associated_user_id;
                    if (user_id == "00000000") return tr.guest_user
                    var user = management.users.get_user(user_id)
                    if (!user) {
                        return tr.user_was_deleted
                    }
                    return user.name
                }
                opacity: 0.6
                color: ui.colors.light1
                textFormat: Text.AutoText
                elide: Text.ElideRight
            }
        }
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
