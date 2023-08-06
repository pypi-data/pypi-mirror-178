import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/js/popups.js" as Popups


Rectangle {
    color: ui.colors.dark3
    Layout.alignment: Qt.AlignTop | Qt.AlignLeft
    Layout.fillWidth: true
    Layout.minimumHeight: 112
    Layout.maximumHeight: 112
    Layout.rightMargin: infoWorkplacesComponent.visible ? 0 : 8

    Item {
        width: parent.width
        height: 96

        Rectangle {
            width: parent.width / 2 - 24
            height: 48
            color: appCompany.filtered_workplaces_model.verification_filter == "VERIFIED" ? ui.colors.dark3 : ui.colors.dark4
            anchors {
                top: parent.top
                left: parent.left
            }

            Custom.FontText {
                text: tr.workplaces_911_approved_tab
                color: appCompany.filtered_workplaces_model.verification_filter == "VERIFIED" ? ui.colors.light3 : ui.colors.middle3
                width: parent.width - 32
                font.pixelSize: 14
                font.bold: true
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 2
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
            }

            Custom.HandMouseArea {
                onClicked: {
                    appCompany.filtered_workplaces_model.set_verification_filter("VERIFIED")
                }
            }
        }

        Rectangle {
            width: parent.width / 2 - 24
            height: 48
            color: appCompany.filtered_workplaces_model.verification_filter == "UNVERIFIED" ? ui.colors.dark3 : ui.colors.dark4
            anchors {
                top: parent.top
                right: parent.right
                rightMargin: 48
            }

            Item {
                width: pendingText.contentWidth + 32
                height: parent.height
                anchors.centerIn: parent

                Custom.FontText {
                    id: pendingText
                    text: tr.unapproved_workplaces
                    color: appCompany.filtered_workplaces_model.verification_filter == "UNVERIFIED" ? ui.colors.light3 : ui.colors.middle3
                    font.pixelSize: 14
                    font.bold: true
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    maximumLineCount: 2
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }
                }

                Rectangle {
                    width: 24
                    height: 24
                    radius: height / 2
                    color: ui.colors.red1
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }

                    visible: appCompany.workplaces_model.pending_count > 0

                    Custom.FontText {
                        text: appCompany.workplaces_model.pending_count
                        font.pixelSize: 12
                        font.weight: Font.Bold
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        anchors.centerIn: parent
                    }
                }
            }

            Custom.HandMouseArea {
                onClicked: {
                    appCompany.filtered_workplaces_model.set_verification_filter("UNVERIFIED")
                }
            }
        }

        Rectangle {
            width: 48
            height: 48
            color: ui.colors.dark4
            anchors {
                top: parent.top
                right: parent.right
            }

            Rectangle {
                width: 1
                height: parent.height
                color: ui.colors.dark3
            }

            Image {
                sourceSize.width: 16
                sourceSize.height: 16
                source: "qrc:/resources/images/icons/settings_green.svg"
                anchors.centerIn: parent
                visible: !settingsLoader.active
            }

            Custom.HandMouseArea {
                enabled: !settingsLoader.active
                onClicked: {
                    app.workplaces_module.get_company_settings()
                }
            }

            Custom.BlockLoading {
                id: settingsLoader
                radius: 8
                minTime: 300
                startSignals: [app.workplaces_module.getCompanySettings]
                stopSignals: [app.workplaces_module.getCompanySettingsSuccess, app.workplaces_module.getCompanySettingsFailed]
            }

            Connections {
                target: app.workplaces_module

                onGetCompanySettingsSuccess: {
                    Popups.company_incident_settings_popup()
                }
            }
        }

        Item {
            width: parent.width
            height: 48
            anchors {
                top: parent.top
                topMargin: 48
            }

            RowLayout {
                id: tabRow
                spacing: 20
                height: 42

                anchors {
                    bottom: parent.bottom
                    bottomMargin: 8
                    left: parent.left
                    leftMargin: 24
                }

                PanelTab {
                    text: tr.a911_all
                    opacity: selected ? 1 : 0.8
                    defaultColor: ui.colors.dark4
                    Layout.minimumHeight: 32
                    Layout.maximumHeight: 32
                    selected: appCompany.filtered_workplaces_model.connection_filter == "ALL"

                    Custom.HandMouseArea {
                        onClicked: {
                            appCompany.filtered_workplaces_model.set_connection_filter("ALL")
                        }
                    }
                }

                PanelTab {
                    text: tr.online
                    opacity: selected ? 1 : 0.8
                    defaultColor: ui.colors.dark4
                    Layout.minimumHeight: 32
                    Layout.maximumHeight: 32
                    selected: appCompany.filtered_workplaces_model.connection_filter == "ONLINE"

                    Custom.HandMouseArea {
                        onClicked: {
                            appCompany.filtered_workplaces_model.set_connection_filter("ONLINE")
                        }
                    }
                }

                PanelTab {
                    text: tr.offline
                    opacity: selected ? 1 : 0.8
                    defaultColor: ui.colors.dark4
                    Layout.minimumHeight: 32
                    Layout.maximumHeight: 32
                    selected: appCompany.filtered_workplaces_model.connection_filter == "OFFLINE"

                    Custom.HandMouseArea {
                        onClicked: {
                            appCompany.filtered_workplaces_model.set_connection_filter("OFFLINE")
                        }
                    }
                }

                PanelTab {
                    text: tr.logged_out_workplaces
                    opacity: selected ? 1 : 0.8
                    defaultColor: ui.colors.dark4
                    Layout.minimumHeight: 32
                    Layout.maximumHeight: 32
                    selected: appCompany.filtered_workplaces_model.connection_filter == "LOGGED_OUT"

                    Custom.HandMouseArea {
                        onClicked: {
                            appCompany.filtered_workplaces_model.set_connection_filter("LOGGED_OUT")
                        }
                    }
                }
            }

            Item {
                id: reloadTabItem
                width: refreshIcon.width + refreshText.width + 4
                height: 32
                anchors {
                    right: parent.right
                    rightMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                Custom.HandMouseArea {
                    onClicked: {
                        refreshAnim.start()
                        app.workplaces_module.get_workplaces()
                    }
                }

                Image {
                    id: refreshIcon
                    sourceSize.width: 16
                    sourceSize.height: 16
                    source: "qrc:/resources/images/desktop/button_icons/refresh.svg"
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    RotationAnimator {
                        id: refreshAnim
                        target: refreshIcon
                        from: 0
                        to: 360
                        duration: 500
                    }
                }

                Custom.FontText {
                    id: refreshText
                    width: contentWidth
                    height: contentHeight
                    text: tr.Refresh_button_desktop
                    color: ui.colors.green1
                    font.bold: true
                    font.pixelSize: 14
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                }
            }
        }
    }

    Rectangle {
        width: parent.width
        height: 1
        color: companyStack.color
        anchors {
            top: parent.top
            topMargin: 96
        }
    }
}
