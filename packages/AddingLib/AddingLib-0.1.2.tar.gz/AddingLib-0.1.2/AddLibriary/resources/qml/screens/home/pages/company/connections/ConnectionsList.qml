import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    color: companyStack.color
    Layout.topMargin: 2
    Layout.alignment: Qt.AlignBottom | Qt.AlignLeft
    Layout.fillHeight: true
    Layout.fillWidth: true
    Layout.rightMargin: infoConnectionsComponent.visible ? 0 : 8
    Layout.minimumHeight: {
        var height = connectionsLayout.height - panel.height - header.height - 10
        if (height > scrollView.contentHeight)
            return scrollView.contentHeight
        return height
    }
    Layout.maximumHeight: Layout.minimumHeight

    property alias connectionsData: connectionsData
    property var lastPosition: 0.0
    property var direction: 0   // 0 - up, 1 - down

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true

        ScrollBar.vertical: Custom.ScrollBar {
            id: control
            parent: scrollView
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            policy: {
                if (scrollView.contentHeight > scrollView.height) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }

            property var prevAB: 0

            onPositionChanged: {
                if (control.position - lastPosition > 0) {
                    direction = 1
                } else {
                    direction = 0
                }
                lastPosition = control.position

                var a = 1 - (control.position + control.size)
                var b = 1 - (control.position + control.size/2)

                if (a/b < 0.4 && direction == 1) {
                    if (prevAB >= 0.4) {
                        panel.filters["a911_channel_state"] = Array.from(panel.filters["a911_channel_state"])
                        panel.filters["binding_state"] = Array.from(panel.filters["binding_state"])
                        panel.filters["translator_channel_state"] = Array.from(panel.filters["translator_channel_state"])
                        app.company_module.get_company_bindings_scroll(panel.filters)
                        app.company_module.get_company_bindings_counter(panel.filters)
                        panel.filters["a911_channel_state"] = new Set(panel.filters["a911_channel_state"])
                        panel.filters["binding_state"] = new Set(panel.filters["binding_state"])
                        panel.filters["translator_channel_state"] = new Set(panel.filters["translator_channel_state"])
                    }
                    if (control.pressed && lastPosition) {
                        control.position = lastPosition
                    }
                }

                control.prevAB = a/b
                }
        }

        ListView {
            id: connectionsData
            spacing: 2
            width: parent.width
            height: parent.height
            property var ownCurrentIndex: -1
            boundsBehavior: Flickable.StopAtBounds
            model: appCompany.filtered_connections_model

            Connections {
                target: infoConnectionsComponent

                onCurrentObjectChanged: {
                    if (!infoConnectionsComponent.currentObject) connectionsData.ownCurrentIndex = -1
                }
            }

            delegate: Item {
                width: parent.width
                height: 56

                Custom.HandMouseArea {
                    anchors.fill: parent
                    onClicked: {
                        connectionsData.ownCurrentIndex = index
                        infoConnectionsComponent.currentObject = connecting
                        header.Layout.rightMargin = 0
                    }
                }

                Custom.RoundedRect {
                    anchors.fill: parent
                    radius: 10
                    color: connectionsData.ownCurrentIndex == index ? "transparent" : ui.colors.dark1
                    bottomRightCorner: connectionsData.ownCurrentIndex - index == 1
                    topRightCorner: {
                        if (connectionsData.ownCurrentIndex < 0) return false
                        return index - connectionsData.ownCurrentIndex == 1
                    }

                    RowLayout {
                        spacing: 8
                        anchors.fill: parent

                        Item {
                            id: bindingItem
                            clip: true
                            Layout.alignment: Qt.AlignLeft
                            Layout.minimumWidth: parent.width / 30 * 3 + 1
                            Layout.maximumWidth: parent.width / 30 * 3 + 1
                            Layout.minimumHeight: parent.height
                            Layout.maximumHeight: parent.height

                            Image {
                                width: 40
                                height: 40
                                source: {
                                    if (connecting && connecting.hub_company_binding_state === "PENDING_DELETION")
                                        return "qrc:/resources/images/icons/hub-removed.svg"
                                    if (connecting && connecting.hub_company_binding_state === "APPROVED")
                                        return "qrc:/resources/images/icons/hub-active.svg"
                                    else
                                        return "qrc:/resources/images/icons/hub-new.svg"
                                }
                                anchors.centerIn: parent
                            }
                        }

                        Item {
                            id: hubIdItem
                            Layout.alignment: Qt.AlignLeft
                            Layout.minimumWidth: parent.width / 30 * 4 + 1
                            Layout.maximumWidth: parent.width / 30 * 4 + 1
                            Layout.minimumHeight: parent.height
                            Layout.maximumHeight: parent.height
                            Layout.leftMargin: 12

                            Custom.FontText {
                                text: connecting ? connecting.hub_id : ""
                                width: parent.width
                                maximumLineCount: 2
                                color: ui.colors.white
                                font.pixelSize: 16
                                wrapMode: Text.WordWrap
                                elide: Text.ElideRight
                                textFormat: Text.AutoText

                                anchors {
                                    verticalCenter: parent.verticalCenter
                                    horizontalCenter: parent.horizontalCenter
                                }
                            }
                        }

                        Item {
                            id: statusItem
                            clip: true
                            Layout.alignment: Qt.AlignLeft
                            Layout.minimumWidth: parent.width / 30 * 3 + 1
                            Layout.maximumWidth: parent.width / 30 * 3 + 1
                            Layout.minimumHeight: parent.height
                            Layout.maximumHeight: parent.height

                            Custom.FontText {
                                text: {
                                    if (connecting) {
                                        if (connecting.a911_channel.state === "ACTIVE")
                                            return tr.binding_status_active
                                        else if (connecting.a911_channel.state === "PENDING_DELETION")
                                            return tr.binding_status_pending_deletion
                                        else
                                            return tr.no_object_911
                                    } else
                                        return ""
                                }
                                width: parent.width
                                color: {
                                    if (connecting && connecting.a911_channel.state === "PENDING_DELETION")
                                        return ui.colors.red1
                                    else if (connecting && connecting.a911_channel.state === "ACTIVE")
                                        return ui.colors.green1
                                    else
                                        return ui.colors.middle1
                                }
                                font.pixelSize: 14
                                wrapMode: Text.WordWrap
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                                maximumLineCount: 2
                                anchors {
                                    verticalCenter: parent.verticalCenter
                                    horizontalCenter: parent.horizontalCenter
                                }
                            }
                        }

                        Item {
                            id: numberItem
                            clip: true
                            Layout.alignment: Qt.AlignLeft
                            Layout.minimumWidth: parent.width / 30 * 4 + 1
                            Layout.maximumWidth: parent.width / 30 * 4 + 1
                            Layout.minimumHeight: parent.height
                            Layout.maximumHeight: parent.height

                            Custom.FontText {
                                text: connecting ? connecting.a911_channel.registration_number: ""
                                width: parent.width
                                color: ui.colors.white
                                font.pixelSize: 14
                                wrapMode: Text.WordWrap
                                elide: Text.ElideRight
                                textFormat: Text.AutoText
                                horizontalAlignment: Text.AlignLeft

                                anchors {
                                    verticalCenter: parent.verticalCenter
                                    left: parent.left
                                }
                            }
                        }

                        Item {
                            id: nameItem
                            Layout.alignment: Qt.AlignLeft
                            Layout.minimumHeight: parent.height
                            Layout.maximumHeight: parent.height
                            Layout.fillWidth: true

                            Custom.FontText {
                                text: connecting ? connecting.a911_channel.name: ""
                                width: parent.width
                                color: ui.colors.white
                                font.pixelSize: 14
                                wrapMode: Text.Wrap
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                                maximumLineCount: 2
                                horizontalAlignment: Text.AlignLeft

                                anchors {
                                    verticalCenter: parent.verticalCenter
                                    left: parent.left
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}