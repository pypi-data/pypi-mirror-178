import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "companyIncidentSettingsPopup"
    width: 528
    height: 312
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

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
            title: tr.generate_incident_setting
            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            closeArea.onClicked: {
                popup.close()
            }
        }

        Item {
            id: body
            width: parent.width - 64
            height: 128
            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
                bottomMargin: 88
            }

            Rectangle {
                width: parent.width
                height: 40
                radius: 10
                clip: true
                color: ui.colors.dark1

                Custom.FontText {
                    text: tr.incident_when_operator_offline
                    width: parent.width - 72
                    color: ui.colors.light3
                    font.pixelSize: 16
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        leftMargin: 16
                        verticalCenter: parent.verticalCenter
                    }
                }

                Custom.Toggle {
                    id: disconnectedToggle

                    anchors {
                        top: parent.top
                        topMargin: 4
                        right: parent.right
                    }

                    checked: {
                        if (!appCompany) return false
                        if (!appCompany.workplaces_model) return false
                        if (!appCompany.workplaces_model.incidents_settings) return false
                        if (!appCompany.workplaces_model.incidents_settings.incident_generation_settings) return false
                        if (!appCompany.workplaces_model.incidents_settings.incident_generation_settings.operator_disconnected) return false

                        if (appCompany.workplaces_model.incidents_settings.incident_generation_settings.operator_disconnected == "ON") return true
                        return false
                    }

                    mouseArea.onClicked: {
                        disconnectedToggle.checked = !disconnectedToggle.checked
                    }
                }
            }

            Rectangle {
                width: parent.width
                height: 40
                radius: 10
                clip: true
                color: ui.colors.dark1
                anchors {
                    bottom: parent.bottom
                    bottomMargin: 32
                }

                Custom.FontText {
                    text: tr.incident_when_unapproved_login
                    width: parent.width - 72
                    color: ui.colors.light3
                    font.pixelSize: 16
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        left: parent.left
                        leftMargin: 16
                        verticalCenter: parent.verticalCenter
                    }
                }

                Custom.Toggle {
                    id: unverifiedToggle

                    anchors {
                        top: parent.top
                        topMargin: 4
                        right: parent.right
                    }

                    checked: {
                        if (!appCompany) return false
                        if (!appCompany.workplaces_model) return false
                        if (!appCompany.workplaces_model.incidents_settings) return false
                        if (!appCompany.workplaces_model.incidents_settings.incident_generation_settings) return false
                        if (!appCompany.workplaces_model.incidents_settings.incident_generation_settings.operator_disconnected) return false

                        if (appCompany.workplaces_model.incidents_settings.incident_generation_settings.unverified_login == "ON") return true
                        return false
                    }

                    mouseArea.onClicked: {
                        unverifiedToggle.checked = !unverifiedToggle.checked
                    }
                }
            }
        }

        Item {
            id: btnSaveItem
            width: parent.width
            height: 88
            anchors.bottom: parent.bottom

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.middle1
                opacity: 0.1
                anchors.right: parent.right
            }

            Anime.SharinganLoader {
                id: anim
                radius: 13
                color: ui.colors.green1
                useCircle: true
                visible: !popup.enabled
                anchors.centerIn: parent
                anchors.verticalCenterOffset: -4
            }

            Item {
                width: parent.width / 2 - 40
                height: 40
                visible: popup.enabled
                anchors {
                    left: parent.left
                    leftMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Custom.Button {
                    width: parent.width
                    text: tr.cancel
                    color: ui.colors.white
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        popup.close()
                    }
                }
            }

            Item {
                width: parent.width / 2 - 40
                height: 40
                visible: popup.enabled
                anchors {
                    right: parent.right
                    rightMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Custom.Button {
                    width: parent.width
                    text: tr.save
                    color: ui.colors.green1
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        popup.enabled = false

                        app.workplaces_module.update_company_settings(disconnectedToggle.checked, unverifiedToggle.checked)
                    }
                }
            }
        }
    }

    Connections {
        target: app.workplaces_module

        onUpdateCompanyIncidentSettingsFailed: {
            popup.enabled = true
        }

        onUpdateCompanyIncidentSettingsSuccess: {
            popup.close()
        }
    }
}
