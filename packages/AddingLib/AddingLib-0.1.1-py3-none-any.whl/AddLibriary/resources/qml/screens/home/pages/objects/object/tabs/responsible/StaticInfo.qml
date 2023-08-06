import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups


Item {
    anchors.fill: parent
    enabled: responsibleTab.isEditable

    property var currentObject: null

    ScrollView {
        clip: true
        width: parent.width - 20
        anchors {
            top: parent.top
            right: parent.right
            bottom: deleteButton.top
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

                visible: responsibleTab.isEditable

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }
//  Version 0.1
//                Custom.UserImage {
//                    id: userImage
//                    width: 80
//                    height: 80
//                    fontSize: 18
//                    imageSource: ""
//                    userName: currentObject ? currentObject.first_name + " " + currentObject.last_name : ""
//                    anchors {
//                        left: parent.left
//                        verticalCenter: parent.verticalCenter
//                    }
//                }

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
                        text: tr.edit
                        transparent: true
                        color: ui.colors.green1
                        anchors.centerIn: parent

                        visible: responsibleTab.isEditable

                        onClicked: {
                            responsibleViewLoader.editMode = true
                        }
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
                    width: parent.width - 24
                    key: tr.name
                    value: currentObject ? currentObject.first_name + " " + currentObject.last_name : ""
                    valueText.font.pixelSize: 18
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

                visible: currentObject.notify_on_issues

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Image {
                    sourceSize.width: 32
                    sourceSize.height: 40
                    source: "qrc:/resources/images/facilities/a-info-badge.svg"
                    anchors {
                        verticalCenter: parent.verticalCenter
                        verticalCenterOffset: -5
                    }
                }

                Custom.FontText {
                    width: parent.width - 48
                    text: tr.a911_inform_about_issues
                    color: ui.colors.white
                    font.pixelSize: 14
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft | Text.AlignVCenter
                    anchors {
                        left: parent.left
                        leftMargin: 40
                        verticalCenter: parent.verticalCenter
                        verticalCenterOffset: -5
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
                        if (!currentObject || currentObject.phone_numbers.length == 0) return tr.a911_unknown
                        var phones = currentObject.phone_numbers
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
                visible: emailField.value != ""

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    id: emailField
                    width: parent.width
                    key: tr.a911_mail
                    distance: 12
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 1
                    value: {
                        if (!currentObject) return ""
                        var temp = currentObject.email_addresses[0]
                        return temp ? temp.email : ""
                    }
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
                Layout.fillHeight: true
            }
        }
    }

    Rectangle {
        id: deleteButton
        color: "transparent"
        width: parent.width
        height: 72
        anchors.bottom: parent.bottom
        visible: responsibleTab.isEditable

        Custom.Button {
            width: parent.width - 32
            text: tr.a911_remove_responsibe_person
            color: ui.colors.red1
            transparent: true
            anchors.centerIn: parent

            visible: responsibleTab.isEditable

            onClicked: {
                if (!currentObject) return

                var settings = {}
                settings["id"] = currentObject.id
                settings["facility_id"] = facility.id

                function task() {
                    app.responsible_person_module.delete_responsible_person(settings)
                }

                Popups.confirmation_deletion_popup(task)
            }
        }
    }
}
