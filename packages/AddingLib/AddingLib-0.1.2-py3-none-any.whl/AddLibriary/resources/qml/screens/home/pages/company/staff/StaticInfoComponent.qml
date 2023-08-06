import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups


Item {
    anchors.fill: parent

    ScrollView {
        id: staffStaticScrollView
        clip: true
        width: parent.width - 20
        anchors {
            top: parent.top
            right: parent.right
            bottom: assignFacilities.top
        }

        ScrollBar.vertical: Custom.ScrollBar {
            parent: staffStaticScrollView
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            policy: {
                if (staffStaticScrollView.contentHeight > staffStaticScrollView.height) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }
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
                Layout.minimumHeight: 112
                Layout.maximumHeight: 112

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.UserImage {
                    id: userImage
                    width: 80
                    height: 80
                    fontSize: 28
                    imageSource: currentObject ? (Object.keys(currentObject.photos).length !== 0 ? currentObject.photos["128x128"] : "") : ""
                    userName: currentObject ? currentObject.data.first_name + " " + currentObject.data.last_name : ""
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }
                }

                Item {
                    width: 150
                    height: 48
                    anchors {
                        top: parent.top
                        topMargin: 12
                        right: parent.right
                        rightMargin: 16
                    }

                    Custom.Button {
                        id: editEmployeeButton

                        width: parent.width
                        text: tr.edit
                        transparent: true
                        color: ui.colors.green1
                        anchors.centerIn: parent
                        visible: currentObject && (
                            appUser.employee_id == currentObject.id
                            || companyAccessAPI.canEditEmployee(JSON.stringify(currentObject.data.role.roles))
                        )

                        onClicked: {
                            application.debug("company -> company info -> employees -> edit employee")
                            editMode = true
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: nameField.valueText.lineCount == 2 ? 104 : 80
                Layout.maximumHeight: nameField.valueText.lineCount == 2 ? 104 : 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    id: nameField
                    width: parent.width
                    key: tr.a911_employee_name
                    value: currentObject ? currentObject.data.first_name + " " + currentObject.data.last_name : ""
                    valueText.font.pixelSize: 18
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 2
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: rolesItem.valueText.lineCount * 20 + 56
                Layout.maximumHeight: rolesItem.valueText.lineCount * 20 + 56

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    id: rolesItem
                    width: parent.width
                    key: tr.a911_role
                    distance: 12
                    valueText.textFormat: Text.PlainText
                    value: {
                        if (!currentObject) return tr.a911_unknown
                        return util.join(app.roles_to_ui(
                            appCompany.company_type == "MONITORING"
                            ? util.remove_installers(currentObject.data.role.roles)
                            : appCompany.company_type == "INSTALLATION"
                            ? util.filter_installation_company_roles(currentObject.data.role.roles)
                            : currentObject.data.role.roles
                        ), "")
                    }
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }

                    Connections {
                        target: tr

                        onTranslation_changed: {
                            rolesItem.value = Qt.binding(function(){
                                if (!currentObject) return tr.a911_unknown
                                return util.join(app.roles_to_ui(currentObject.data.role.roles), "")
                            })
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: phoneText.height + 24
                Layout.maximumHeight: phoneText.height + 24

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    id: phoneText
                    width: parent.width
                    key: tr.phone
                    value: {
                        if (!currentObject || currentObject.data.phone_numbers.length == 0) return tr.a911_unknown
                        var phones = currentObject.data.phone_numbers
                        var _ph = []
                        for(var i=0; i < phones.length; i++) {
                            _ph.push(phones[i].number)
                        }
                        return _ph.join("<br>")
                    }
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.a911_login
                    distance: 12
                    value: currentObject ? currentObject.data.email : ""
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                }
            }

//            Rectangle {
//                color: "transparent"
//                Layout.fillWidth: true
//                Layout.minimumHeight: 80
//                Layout.maximumHeight: 80
//
//                Custom.TextFieldStatic {
//                    width: parent.width
//                    key: currentObject ? "User ID " + currentObject.data.id : ""
//                    distance: 12
//                    value: ""
//                    anchors {
//                        top: parent.top
//                        topMargin: 12
//                        left: parent.left
//                    }
//                    // copyItem.visible: false
//                }
//            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }

    Rectangle {
        id: assignFacilities
        clip: true
        color: "transparent"
        width: parent.width
        height: visible ? 56 : 0
        anchors.bottom: deleteButton.top

        property var functionalSettingsOn: {
            if (!appCompany) return false
            if (!appCompany.workplaces_model) return false
            if (!appCompany.workplaces_model.incidents_settings) return false
            if (!appCompany.workplaces_model.incidents_settings.facility_permission_settings) return false
            if (!appCompany.workplaces_model.incidents_settings.facility_permission_settings.full_access) return false

            if (appCompany.workplaces_model.incidents_settings.facility_permission_settings.full_access == "ON") return true
            return false
        }

        visible: {
            if (!appCompany.data.provided_services.installation) return false
            if (!companyAccess.OBJECT_EMPLOYEE_ASSIGN) return false

            if (!currentObject) return false
            if (!currentObject.data) return false
            if (!currentObject.data.role) return false
            if (!currentObject.data.role.roles) return false
            if (assignFacilities.functionalSettingsOn) return false
            if (!editEmployeeButton.visible) return false
            if (appUser.employee_id == currentObject.id) return false

            return currentObject.data.role.roles.includes("INSTALLER")
                   && !currentObject.data.role.roles.includes("HEAD_OF_INSTALLERS")
        }

        Custom.Button {
            id: assignButton
            width: parent.width - 32
            text: tr.assigned_object
            transparent: true
            color: ui.colors.green1
            loading_background_color: ui.colors.dark3
            anchors.centerIn: parent

            onClicked: {
                application.debug("company -> company info -> employees -> assign facilities")

                Popups.facilities_permissions_popup(currentObject)
            }
        }
    }

    Rectangle {
        id: deleteButton
        color: "transparent"
        width: parent.width
        height: deleteButtonItem.visible ? 72 : 8
        anchors.bottom: parent.bottom

        Custom.Button {
            id: deleteButtonItem
            width: parent.width - 32
            text: tr.a911_delete_profile

            color: ui.colors.dark4
            textButton.color: ui.colors.white
            visible: currentObject && (
                appUser.employee_id != currentObject.id
                && companyAccessAPI.canEditEmployee(JSON.stringify(currentObject.data.role.roles))
            )
            transparent: false
            anchors.centerIn: parent

            onClicked: {
                application.debug("company -> company info -> employees -> delete employee")
                if (!currentObject) return

                var settings = {}
                settings["id"] = currentObject.id

                function task() {
                    app.employee_module.delete_employee(settings)
                }

                Popups.confirmation_deletion_popup(task)
            }
        }
    }
}
