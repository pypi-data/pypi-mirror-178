import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "create911ChannelPopup"
    width: 384
    height: header.height + body.height + btnSaveItem.height + 48
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    property var settings: null
    property var mode: null

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        radius: 8
        color: ui.colors.dark3
        anchors.fill: parent

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.a911_add_object
            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            closeArea.onClicked: {
                popup.close()
            }

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.middle1
                opacity: 0.1
                anchors {
                    right: parent.right
                    bottom: parent.bottom
                }
            }
        }

        ColumnLayout {
            id: body
            width: parent.width - 64
            anchors{
                top: header.bottom
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                Layout.topMargin: 8

                Custom.TextFieldEdit {
                    id: objectNumber
                    distance: 20
                    width: parent.width
                    valueText.control.validator: RegExpValidator { regExp : /\S+/ }
                    valueText.control.maximumLength: 10
                    valueText.control.font.pixelSize: 16
                    valueText.control.color: ui.colors.light3
                    key: tr.account_number + ui.required
                    value: {
                        if (!popup.settings) return ""
                        if (!popup.settings.registration_number) return ""
                        return popup.settings.registration_number
                    }
                }
            }

            Rectangle{
                color: "transparent"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                Layout.topMargin: 8

                Custom.TextFieldEdit {
                    id: objectName
                    distance: 20
                    width: 320
                    valueText.control.maximumLength: 200
                    valueText.control.font.pixelSize: 16
                    valueText.control.color: ui.colors.light3
                    key: tr.object_name + ui.required
                    value: {
                        if (!popup.settings) return ""
                        if (!popup.settings.name) return ""
                        return popup.settings.name
                    }
                }
            }

            Rectangle{
                color: "transparent"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                Layout.topMargin: 8

                Custom.TextFieldEdit {
                    id: objectHubId
                    distance: 20
                    width: 320
                    enabled: false
                    opacity: enabled ? 1 : 0.7
                    valueText.control.maximumLength: 200
                    valueText.control.font.pixelSize: 16
                    valueText.control.color: ui.colors.light3
                    key: tr.a911_hub_id + ui.required
                    value: {
                        if (!popup.settings) return ""
                        if (!popup.settings.hub_id) return ""
                        return popup.settings.hub_id
                    }
                }
            }
        }

        Item {
            id: btnSaveItem
            width: parent.width
            height: 88
            anchors {
                top: body.bottom
                topMargin: 24
            }

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.middle1
                opacity: 0.1
                anchors.right: parent.right
            }

            Custom.Button {
                id: btnSave
                width: parent.width - 64
                text: tr.next
                enabledCustom: objectName.valueText.control.text != "" && objectNumber.valueText.control.text != ""
                anchors.centerIn: parent

                onClicked: {
                    var settingsData = {}

                    settingsData["registration_number"] = objectNumber.valueText.control.text
                    settingsData["name"] = objectName.valueText.control.text
                    settingsData["hub_id"] = objectHubId.valueText.control.text
                    settingsData["facility_id"] = popup.settings["facility_id"]

                    popup.enabled = false
                    loading = true

                    if (popup.mode == "facility") {
                        app.facility_module.create_channel_911(settingsData)
                    } else {
                        app.bindings_module.create_channel_911(settingsData)
                    }
                }
            }
        }
    }

    Connections {
        target: app.facility_module

        onCreateChannel911Success: {
            // back to connect table if necessary
            if (objectsStack.currentObjectIndex != -1) {
                objectsStack.currentObjectIndex = -1
            } else {
                objectsSidebar.reloadModel()
            }

            // to open edit tab: objectsStack.currentObjectIndex = -3
            var editModeIndex = companyAccess.OBJECT_CARD_EDIT ? -3 : -2

            app.facility_module.get_facility(facility_id, editModeIndex)
            popup.close()
        }

        onCreateChannel911Failed: {
            btnSave.loading = false
            popup.enabled = true
        }
    }

    Connections {
        target: app.bindings_module

        onCreateChannel911Success: {
            var settingsData = {}
            settingsData["hub_id"] = hub_id

            app.bindings_module.get_hub_company_binding(settingsData)
            popup.close()
        }

        onCreateChannel911Failed: {
            btnSave.loading = false
            popup.enabled = true
        }
    }
}
