import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "createWorkplacePopup"
    width: 328
    height: header.height + body.height + btnSaveItem.height + 48
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    property var workplace: null
    property var incident_id: null

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    onOpened: {
        if (objectNumber.enabled) {
            objectNumber.valueText.control.forceActiveFocus()
        } else {
            objectName.valueText.control.forceActiveFocus()
        }
    }

    contentItem: Rectangle {
        radius: 10
        color: ui.colors.dark3
        anchors.fill: parent

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.add_workplace
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
            anchors {
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
                    enabled: false
                    width: parent.width
                    valueText.control.font.pixelSize: 16
                    valueText.control.color: ui.colors.light3
                    key: tr.machine_id + ui.required
                    value: popup.workplace.machine_id
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                Layout.topMargin: 8

                Custom.TextFieldEdit {
                    id: objectName
                    distance: 20
                    width: 256
                    valueText.control.maximumLength: 100
                    valueText.control.font.pixelSize: 16
                    valueText.control.color: ui.colors.light3
                    key: tr.workplaces_911_popup + ui.required
                    value: popup.workplace.name

                    Connections {
                        target: app.workplaces_module

                        onValidationErrors: {
                            if (result["3"]) {
                                objectName.valueText.valid = false
                                objectName.valueText.error = result["3"].message
                            }
                        }
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
                enabledCustom: objectName.valueText.control.text != "" && objectNumber.valueText.control.text.length >= 3
                anchors.centerIn: parent

                onClicked: {
                    var settings = {}

                    settings["workplace"] = popup.workplace
                    settings["name"] = objectName.valueText.control.text

                    popup.enabled = false
                    loading = true

                    if (!popup.incident_id) {
                        app.workplaces_module.create_workplace(settings)
                    } else {
                        app.workplaces_module.create_incident_workplace(settings, popup.incident_id)
                    }
                }
            }
        }
    }

    Connections {
        target: app

        onActionFailed: {
            btnSave.loading = false
            popup.enabled = true
        }
    }

    Connections {
        target: app.workplaces_module

        onCreateWorkplaceSuccess: {
            popup.close()
        }

        onCreateWorkplaceFailed: {
            btnSave.loading = false
            popup.enabled = true
        }
    }
}
