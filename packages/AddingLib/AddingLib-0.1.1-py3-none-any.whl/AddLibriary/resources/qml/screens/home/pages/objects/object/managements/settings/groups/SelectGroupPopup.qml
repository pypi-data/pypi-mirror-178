import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views" as View
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/"

import "qrc:/resources/js/desktop/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 360
    height: 410

    modal: true
    focus: true

    closePolicy: Popup.NoAutoClose | Popup.CloseOnEscape

    property var devices: []

    Rectangle {
        width: 360
        height: 410
        color: "#252525"

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        AjaxPopupCloseHeader {
            id: closeItem
            fontSize: 14
            textOpacity: 0.6
            label: ""
        }

        View.List {
            id: groupsView
            width: popup.width
            anchors {
                top: closeItem.bottom
                bottom: mouseArea.top
            }
            spacing: 0
            model: groups

            cacheBuffer: 2000

            currentIndex: -1

            delegate: Item {
                width: rect.width
                height: 64

                Rectangle {
                    id: sigRect
                    width: 3
                    height: parent.height
                    visible: false
                    color: ui.colors.green1
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        parent.opacity = 1.0
                        sigRect.visible = true
                    }
                    onExited: {
                        parent.opacity = 0.8
                        sigRect.visible = false
                    }

                    onClicked: {
                        groupsView.currentIndex = index
                    }
                }

                Image {
                    width: 32
                    height: 32
                    visible: groupsView.currentIndex == index
                    source: "qrc:/resources/images/desktop/icons/check@2x.png"
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 64
                }

                Rectangle {
                    anchors.top: parent.top
                    height: 1
                    width: parent.width
                    color: ui.colors.light1
                    opacity: 0.1
                }

                Rectangle {
                    anchors.top: parent.bottom
                    height: 1
                    width: parent.width
                    color: ui.colors.light1
                    opacity: 0.1
                    visible: (groups.length - 1 == index) ? true : false
                }

                Group {
                    width: rect.width
                }
            }
        }

        MouseArea {
            id: mouseArea
            width: parent.width
            height: 48

            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            Rectangle {
                width: parent.width
                height: 1
                opacity: 0.1
                color: ui.colors.light1

                anchors.top: parent.top
            }

            Text {
                anchors.centerIn: parent
                text: tr.add_devices_to_group
                color: ui.colors.green1
                font.family: roboto.name
                font.pixelSize: 14
            }

            anchors {
                bottom: parent.bottom
            }

            onClicked: {
                if (groupsView.currentIndex == -1) return
                var group = groups.get(groupsView.currentIndex)

                if (!group) return
                for (var i = 0; i < devices.length; i++) {
                    devices[i].group_id = group.id
                }

                app.hub_management_module.update_objects_settings(devices)
            }
        }
    }

    Connections {
        target: app
        onActionSuccess: {
            popup.close()
        }
    }
}