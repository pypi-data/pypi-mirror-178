import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups


Item {
    anchors.fill: parent

    Rectangle {
        id: scrollView
        width: parent.width
        height: 390
        color: ui.colors.dark3
        anchors {
            top: parent.top
            right: parent.right
        }

        ColumnLayout {
            spacing: 10
            width: parent.width
            anchors {
                top: parent.top
                right: parent.right
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80
                Layout.topMargin: 32

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors {
                        bottom: parent.bottom
                        left: parent.left
                        leftMargin: 20
                    }
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.object_name
                    value: currentObject ? currentObject.a911_channel.name : ""
                    valueText.font.pixelSize: 24
                    valueText.color: ui.colors.light3
                    valueText.leftPadding: 20
                    keyText.leftPadding: 20
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 1
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 56
                Layout.maximumHeight: 56

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors {
                        bottom: parent.bottom
                        left: parent.left
                        leftMargin: 20
                    }
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.a911_hub_id
                    distance: 6
                    value: currentObject ? currentObject.hub_id : ""
                    valueText.leftPadding: 20
                    keyText.leftPadding: 20
                    anchors {
                        top: parent.top
                        topMargin: 6
                        left: parent.left
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 56
                Layout.maximumHeight: 56

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors {
                        bottom: parent.bottom
                        left: parent.left
                        leftMargin: 20
                    }
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.account_number
                    distance: 6
                    valueText.leftPadding: 20
                    keyText.leftPadding: 20
                    value: currentObject ? currentObject.a911_channel.registration_number : ""
                    anchors {
                        top: parent.top
                        topMargin: 6
                        left: parent.left
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 136
                Layout.maximumHeight: 136

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors {
                        bottom: parent.bottom
                        left: parent.left
                    }
                    color: ui.colors.black
                }

                Custom.TextFieldStatic {
                    id: phoneText
                    width: parent.width
                    key: tr.a911_binding_status
                    value: {
                        if (currentObject) {
                            if (currentObject.a911_channel.state === "ACTIVE")
                                return tr.binding_status_active
                            else if (currentObject.a911_channel.state === "PENDING_DELETION")
                                return tr.binding_status_pending_deletion
                            else
                                return tr.no_object_911
                        }
                        return ""
                    }
                    valueText.leftPadding: 20
                    keyText.leftPadding: 20
                    distance: 6
                    valueText.color: {
                        if (currentObject) {
                            if (currentObject.a911_channel.state === "PENDING_DELETION")
                                return ui.colors.red1
                            else if (currentObject.a911_channel.state === "ACTIVE")
                                return ui.colors.green1
                            else
                                return ui.colors.middle1
                        }
                        return ui.colors.middle1
                    }
                    anchors {
                        top: parent.top
                        topMargin: 6
                        left: parent.left
                    }
                }

                Custom.Button {
                    id: controlButton
                    width: 98
                    text: {
                        if (currentObject) {
                            if (currentObject.a911_channel.state === "ACTIVE" || currentObject.a911_channel.state === "PENDING_DELETION")
                                return tr.go_to_object
                        }
                        return tr.add
                    }
                    color: ui.colors.green1
                    transparent: true
                    anchors {
                        top: phoneText.bottom
                        topMargin: 8
                        left: parent.left
                        leftMargin: 20
                    }

                     onClicked: {
                        if (currentObject) {
                            if (controlButton.text == tr.go_to_object) {
                                controlButton.enabled = false
                                timer.start()
                                if (objectsStack.currentObjectIndex != -4) objectsStack.currentObjectIndex = -4
                                app.facility_module.get_facility(currentObject.a911_channel.facility_id, -5)
                            }
                            else if (controlButton.text == tr.add) {
                                var settingsData = {}
                                settingsData["hub_id"] = currentObject.hub_id ? currentObject.hub_id : ""
                                settingsData["registration_number"] = ""
                                settingsData["name"] = ""

                                if (currentObject.a911_channel) {
                                    settingsData["registration_number"] = currentObject.a911_channel.registration_number ? currentObject.a911_channel.registration_number : ""
                                    settingsData["name"] = currentObject.a911_channel.name ? currentObject.a911_channel.name : ""
                                }

                                Popups.add_object_popup(true, settingsData.hub_id, settingsData.name, settingsData.registration_number, currentObject.hub_company_binding_state)
                            }
                        }
                     }
                    Timer {
                        id: timer
                        running: false
                        repeat: false
                        interval: 1000
                        onTriggered: controlButton.enabled = true
                    }
                }

                Custom.Button {
                    id: restoreButton
                    width: currentObject && currentObject.a911_channel.state === "PENDING_DELETION" ? 132 : 0
                    text: tr.restore_object
                    color: ui.colors.white
                    visible: currentObject && currentObject.a911_channel.state === "PENDING_DELETION"
                    transparent: true
                    anchors {
                        top: phoneText.bottom
                        topMargin: 8
                        left: controlButton.right
                        leftMargin: currentObject && currentObject.a911_channel.state === "PENDING_DELETION" ? 8 : 0
                    }

                     onClicked: {
                        app.company_module.cancel_channel_911_removal(currentObject)
                     }
                }

                Item {
                    id: deleteIcon
                    width: 40
                    height: parent.height
                    anchors {
                        top: restoreButton.top
                        left: restoreButton.right
                        leftMargin: 8
                    }

                    Image {
                        id: imageDelete
                        sourceSize.width: 40
                        sourceSize.height: 40
                        visible: currentObject && (currentObject.a911_channel.state === "PENDING_DELETION" || currentObject.a911_channel.state === "ACTIVE")
                        source: {
                            if (currentObject) {
                                if (currentObject.a911_channel.state === "ACTIVE")
                                    return "qrc:/resources/images/icons/delete_with_circle.svg"
                                else {
                                    var url = "";
                                    if (currentObject.a911_channel.active_until === 6) {
                                        url = "qrc:/resources/images/icons/delete-immediately-6-days-left.svg"
                                    } else if (currentObject.a911_channel.active_until === 5) {
                                        url = "qrc:/resources/images/icons/delete-immediately-5-days-left.svg"
                                    } else if (currentObject.a911_channel.active_until === 4) {
                                        url = "qrc:/resources/images/icons/delete-immediately-4-days-left.svg"
                                    } else if (currentObject.a911_channel.active_until === 3) {
                                        url = "qrc:/resources/images/icons/delete-immediately-3-days-left.svg"
                                    } else if (currentObject.a911_channel.active_until === 2) {
                                        url = "qrc:/resources/images/icons/delete-immediately-2-days-left.svg"
                                    } else if (currentObject.a911_channel.active_until === 1) {
                                        url = "qrc:/resources/images/icons/delete-immediately-1-days-left.svg"
                                    } else
                                        url = "qrc:/resources/images/icons/delete-immediately-7-days-left.svg"
                                    return url
                                }
                            }
                            return ""
                        }

                        Custom.HandMouseArea {
                            id: deleteArea
                            hoverEnabled: true

                            onClicked: {
                                if (imageDelete.source == "qrc:/resources/images/icons/delete_with_circle.svg")
                                    Popups.delete_translator_facility_popup(tr.move_object_to_trash, "SCHEDULE")
                                else
                                    Popups.delete_translator_facility_popup(tr.a911_delete_object_permanently, "REMOVE")
                            }

                            ToolTip {
                                id: tooltip
                                parent: imageDelete
                                visible: deleteArea.containsMouse && imageDelete.source != "qrc:/resources/images/icons/delete_with_circle.svg"

                                contentItem: Text {
                                    text: currentObject && currentObject.a911_channel.active_until ? util.insert(tr.time_before_deleting, [currentObject.a911_channel.active_until]) : util.insert(tr.time_before_deleting, [7])
                                    font.family: roboto.name
                                    font.pixelSize: 12
                                    color: ui.colors.light3
                                }

                                background: Rectangle {
                                    color: ui.colors.dark2
                                    radius: 8
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    Item {
        id: translatorBlock
        width: parent.width
        anchors {
            top: scrollView.bottom
            right: parent.right
            bottom: deleteButtonRect.top
        }

        ColumnLayout {
            spacing: 10
            width: parent.width
            anchors {
                top: parent.top
                right: parent.right
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 56
                Layout.maximumHeight: 56

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors {
                        bottom: parent.bottom
                        left: parent.left
                        leftMargin: 20
                    }
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.translator_binding_status
                    distance: 6
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.leftPadding: 20
                    keyText.leftPadding: 20
                    value: {
                        if (currentObject && currentObject.translator_channel.state === "ACTIVE")
                            return tr.binding_status_active
                        else
                            return tr.no_object_911
                    }
                    valueText.color: {
                        if (currentObject && currentObject.translator_channel.state === "ACTIVE")
                            return ui.colors.green1
                        else
                            return ui.colors.middle1
                    }
                    anchors {
                        top: parent.top
                        topMargin: 6
                        left: parent.left
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 56
                Layout.maximumHeight: 56

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors {
                        bottom: parent.bottom
                        left: parent.left
                        leftMargin: 20
                    }
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.company_binding_status
                    distance: 6
                    value: {
                        if (currentObject && currentObject.hub_company_binding_state === "APPROVED")
                            return tr.binding_status_approver
                        else if (currentObject && currentObject.hub_company_binding_state === "PENDING_DELETION")
                            return tr.binding_status_pending_deletion
                        else if (currentObject && currentObject.hub_company_binding_state === "PENDING_APPROVAL")
                            return tr.binding_status_pending_approval
                        else
                            return tr.no_object_911
                    }
                    valueText.leftPadding: 20
                    keyText.leftPadding: 20
                    valueText.color: {
                        if (currentObject && currentObject.hub_company_binding_state === "PENDING_APPROVAL")
                            return ui.colors.yellow1
                        else if (currentObject && currentObject.hub_company_binding_state === "APPROVED")
                            return ui.colors.green1
                        else
                            return ui.colors.red1
                    }
                    anchors {
                        top: parent.top
                        topMargin: 6
                        left: parent.left
                    }
                }
            }
        }
    }

    Rectangle {
        id: deleteButtonRect
        color: "transparent"
        width: parent.width
        height: deleteButton.height
        anchors {
            bottom: parent.bottom
            bottomMargin: 32
        }

        Custom.Button {
            id: deleteButton
            width: parent.width - 32
            text: tr.delete_binding
            color: ui.colors.dark3
            textButton.color: ui.colors.white
            anchors.centerIn: parent

            onClicked: {
                application.debug("company -> connections -> delete hub")

                Popups.delete_translator_facility_popup(tr.delete_hub_company_binding, "BINDING")
            }
        }
    }
}