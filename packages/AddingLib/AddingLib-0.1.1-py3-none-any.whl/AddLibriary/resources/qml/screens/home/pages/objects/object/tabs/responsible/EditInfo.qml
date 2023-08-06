import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    anchors.fill: parent

    property var addPerson: false
    property var currentObject: null

    ScrollView {
        clip: true
        width: parent.width - 20
        anchors {
            top: parent.top
            right: parent.right
            bottom: saveButton.top
        }

        ColumnLayout {
            spacing: 4
            width: parent.width
            anchors {
                top: parent.top
                right: parent.right
            }
// Version 0.1
//            Rectangle {
//                color: "transparent"
//                Layout.fillWidth: true
//                Layout.minimumHeight: 112
//                Layout.maximumHeight: 112
//
//                Rectangle {
//                    height: 1
//                    width: parent.width
//                    anchors.bottom: parent.bottom
//                    color: ui.colors.white
//                    opacity: 0.1
//                }
//
//                Custom.UserImage {
//                    id: userImageEdit
//                    width: 80
//                    height: 80
//                    fontSize: 18
//                    imageSource: ""
//                    editing: true
//                    userName: currentObject ? currentObject.first_name + " " + currentObject.last_name : ""
//                    anchors {
//                        left: parent.left
//                        verticalCenter: parent.verticalCenter
//                    }
//                }
//
//                Item {
//                    width: 150
//                    height: 48
//                    visible: !addPerson
//                    anchors {
//                        top: parent.top
//                        topMargin: 12
//                        right: parent.right
//                        rightMargin: 16
//                    }
//
//                    Custom.Button {
//                        width: parent.width
//                        text: tr.cancel
//                        transparent: true
//                        color: ui.colors.white
//                        anchors.centerIn: parent
//
//                        onClicked: {
//                            responsibleViewLoader.editMode = false
//                        }
//                    }
//                }
//            }


            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: visible ? 72 : 0
                Layout.maximumHeight: visible ? 72 : 0
                visible: !addPerson

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
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
                        width: parent.width
                        text: tr.cancel
                        transparent: true
                        color: ui.colors.white
                        anchors.centerIn: parent

                        onClicked: {
                            responsibleViewLoader.editMode = false
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 88
                Layout.maximumHeight: 88

                Custom.TextFieldEdit {
                    id: userFirstName
                    width: parent.width - 16
                    key: tr.a911_name_surname + ui.required
                    value: currentObject ? currentObject.first_name : ""
                    valueText.control.maximumLength: 200
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
                Layout.minimumHeight: 96
                Layout.maximumHeight: 96

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldEdit {
                    id: userLastName
                    width: parent.width - 16
                    key: tr.last_name + ui.required
                    value: currentObject ? currentObject.last_name : ""
                    valueText.control.maximumLength: 100
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }

                    Connections {
                        target: app.responsible_person_module
                        onResponsiblePersonChangeError: {
                            if (result['6']) {
                                userLastName.valueText.valid = false
                                userLastName.valueText.error = result['6'].message
                            }
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: informAboutIssues.lineCount == 1 ? 80 : 88
                Layout.maximumHeight: informAboutIssues.lineCount == 1 ? 80 : 88

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Image {
                    id: notifyField
                    sourceSize.width: 32
                    sourceSize.height: 40
                    source: notifyEnabled ? "qrc:/resources/images/facilities/a-badge-green.svg" : "qrc:/resources/images/facilities/a-badge-default.svg"
                    anchors {
                        top: parent.top
                        topMargin: 8
                    }

                    property var notifyEnabled: currentObject ? currentObject.notify_on_issues : false

                    Custom.HandMouseArea {
                        onClicked: {
                            notifyField.notifyEnabled = !notifyField.notifyEnabled
                        }
                    }
                }

                Custom.FontText {
                    id: informAboutIssues
                    width: parent.width - 48
                    text: tr.a911_inform_about_issues
                    color: ui.colors.white
                    font.pixelSize: 14
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    horizontalAlignment: Text.AlignLeft | Text.AlignVCenter
                    anchors {
                        top: parent.top
                        topMargin: 10
                        left: parent.left
                        leftMargin: 44
                    }
                }

                Custom.FontText {
                    width: parent.width - 48
                    text: tr.show_user_on_monitoring_screen
                    color: ui.colors.middle3
                    font.pixelSize: 12
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft | Text.AlignVCenter
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: 16
                        left: parent.left
                        leftMargin: 44
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: phoneEditField.height + 12
                Layout.maximumHeight: phoneEditField.height + 12

                Custom.PhonesEdit {
                    id: phoneEditField
                    width: parent.width - 16
                    key: tr.phone + ui.required
                    distance: 12
                    withType: false
                    model: currentObject ? currentObject.phone_numbers : []
                    maxPhoneNumbers: 3
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    Connections {
                        target: app.responsible_person_module
                        onResponsiblePersonChangeError: {
                            phoneEditField.errorsResult(result)
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: userLogin.height + 12
                Layout.maximumHeight: userLogin.height + 12

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldEdit {
                    id: userLogin
                    width: parent.width - 16
                    key: tr.a911_mail
                    value: {
                        if (!currentObject) return ""
                        var temp = currentObject.email_addresses[0]
                        return temp ? temp.email : ""
                    }
                    valueText.control.maximumLength: 100
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    Connections {
                        target: app.responsible_person_module
                        onResponsiblePersonChangeError: {
                            if (result['10[0].1']) {
                                userLogin.valueText.valid = false
                                userLogin.valueText.error = result['10[0].1'].message
                            }
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }

    Rectangle {
        id: saveButton
        width: parent.width
        height: 104
        color: ui.colors.dark3
        anchors.bottom: parent.bottom

        Custom.Button {
            width: parent.width - 32
            text: tr.save_scenario
            transparent: false
            color: ui.colors.green1
            anchors.centerIn: parent
            enabled: userFirstName.valueText.control.text.length > 0
                     && userLastName.valueText.control.text.length > 0
                     && phoneEditField.phonesAreNotEmpty

            onClicked: {
                saveButton.forceActiveFocus()
                var phones = []
                phoneEditField.listView.model.forEach(function(phone) {
                    phones.push(phone)
                })

                var settings = {}
                settings["first_name"] = userFirstName.valueText.control.text
                settings["last_name"] = userLastName.valueText.control.text
                settings["notify_on_issues"] = notifyField.notifyEnabled
                settings["phone_numbers"] = phones
                if (userLogin.valueText.control.text == "") {
                    settings["email_addresses"] = []
                } else {
                    settings["email_addresses"] = [{"email": userLogin.valueText.control.text}]
                }

                if (addPerson) {
                    app.responsible_person_module.create_responsible_person(settings)
                    return
                }
                app.responsible_person_module.update_responsible_person(currentObject, settings)
            }
        }
    }

    Component.onCompleted: {
        if (!facility.id) return

        userFirstName.valueText.control.forceActiveFocus()
    }

    Connections {
        target: appCompany.current_facility.responsible_persons

        onActionSuccess: {
            if (addPerson) return
            responsibleViewLoader.editMode = false
        }
    }
}