import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "addInstallersPopup"
    width: 420
    height: 632
    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true

    anchors.centerIn: parent

    property var facility: null
    property var installersModel: null

    onOpened: {
        app.employee_module.search_installers({})
    }

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 8

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: ""
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }

            Custom.FontText {
                id: headerText

                text: tr.add_new_installer
                color: ui.colors.light3
                width: parent.width - 128
                height: 24

                font.pixelSize: 16
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors {
                    top: parent.top
                    topMargin: 24
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Custom.FontText {
                id: facilityNameNumber

                color: ui.colors.middle3
                width: parent.width - 128
                height: 16
                visible: !truncated

                font.pixelSize: 12
                wrapMode: Text.NoWrap
                elide: Text.ElideMiddle
                textFormat: Text.PlainText
                maximumLineCount: 1
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors {
                    top: parent.top
                    topMargin: 56
                    horizontalCenter: parent.horizontalCenter
                }

                text: {
                    var tmpName = ""
                    var tmpNumber = ""
                    var tmpDiv = "  •  № "

                    if (!popup.facility) return ui.empty + tmpDiv + ui.empty
                    if (!popup.facility.data) return ui.empty + tmpDiv + ui.empty

                    tmpName = facility.data.facility_general_info ? facility.data.facility_general_info.name : facility.data.hub_id
                    tmpName = tmpName ? tmpName : ui.empty

                    tmpNumber = facility.data.facility_general_info ? facility.data.facility_general_info.registration_number : ui.empty
                    tmpNumber = tmpNumber ? tmpNumber : ui.empty

                    return tmpName + tmpDiv + tmpNumber
                }
            }

            Custom.FontText {
                id: facilityName

                color: ui.colors.middle3
                width: parent.width - 128
                height: 16
                visible: facilityNameNumber.truncated

                font.pixelSize: 12
                wrapMode: Text.NoWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors {
                    top: parent.top
                    topMargin: 56
                    horizontalCenter: parent.horizontalCenter
                }

                text: {
                    if (!popup.facility) return ui.empty
                    if (!popup.facility.data) return ui.empty

                    var tmpName = facility.data.facility_general_info ? facility.data.facility_general_info.name : facility.data.hub_id
                    return tmpName ? tmpName : ui.empty
                }
            }

            Custom.FontText {
                id: facilityNumber

                color: ui.colors.middle3
                width: parent.width - 128
                height: 16
                visible: facilityNameNumber.truncated

                font.pixelSize: 12
                wrapMode: Text.NoWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors {
                    top: parent.top
                    topMargin: 72
                    horizontalCenter: parent.horizontalCenter
                }

                text: {
                    if (!popup.facility) return ui.empty
                    if (!popup.facility.data) return ui.empty

                    var tmpNumber = facility.data.facility_general_info ? facility.data.facility_general_info.registration_number : ui.empty
                    return tmpNumber ? tmpNumber : ui.empty
                }
            }
        }

        ColumnLayout {
            width: parent.width - 148
            spacing: 16
            anchors {
                top: header.bottom
                topMargin: 24
                bottom: parent.bottom
                bottomMargin: 24
                horizontalCenter: parent.horizontalCenter
            }

            Rectangle {
                color: "transparent"
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80
                Layout.fillWidth: true

                Custom.FontText {
                    id: installerKeyText
                    text: tr.choose_installer + ui.required
                    width: parent.width
                    color: ui.colors.white
                    opacity: 0.5
                    font.pixelSize: 14
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        top: parent.top
                        topMargin: 0
                        left: parent.left
                    }
                }

                Custom.InstallersCombobox {
                    id: installerValueText
                    width: parent.width
                    defaultText: tr.choose_installer_tip

                    model: popup.installersModel ? popup.installersModel.employees : []

                    anchors {
                        top: installerKeyText.bottom
                        topMargin: 12
                        left: parent.left
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumHeight: 304
                Layout.maximumHeight: 304
                Layout.fillWidth: true

                Custom.FontText {
                    id: permissionsText
                    text: tr.permissions + ui.required
                    width: parent.width
                    color: ui.colors.white
                    opacity: 0.5
                    font.pixelSize: 14
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        top: parent.top
                        left: parent.left
                    }
                }

                Column {
                    width: parent.width
                    anchors {
                        top: permissionsText.bottom
                        topMargin: 16
                        left: parent.left
                    }

                    Repeater {
                        id: accessRepeater
                        model: ["NO_ACCESS", "1_HOUR", "2_HOURS", "4_HOURS", "8_HOURS", "PERMANENT_ACCESS"]

                        property var currentAccess: "NO_ACCESS"

                        delegate: Item {
                            width: parent.width
                            height: 48

                            Rectangle {
                                width: parent.width
                                height: 40
                                radius: 8
                                color: ui.colors.dark1

                                Custom.FontText {
                                    maximumLineCount: 1
                                    color: ui.colors.light3
                                    font.pixelSize: 16
                                    wrapMode: Text.NoWrap
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    horizontalAlignment: Text.AlignLeft
                                    verticalAlignment: Text.AlignVCenter
                                    anchors {
                                        left: parent.left
                                        leftMargin: 16
                                        verticalCenter: parent.verticalCenter
                                    }

                                    text: {
                                        if (modelData == "NO_ACCESS") return tr.no_pro_permissions
                                        if (modelData == "1_HOUR") return "1 " + tr.hour
                                        if (modelData == "2_HOURS") return "2 " + tr.hours
                                        if (modelData == "4_HOURS") return "4 " + tr.hours
                                        if (modelData == "8_HOURS") return "8 " + tr.hours
                                        if (modelData == "PERMANENT_ACCESS") return tr.permanent_access
                                        return ""
                                    }
                                }

                                Image {
                                    sourceSize.width: 32
                                    sourceSize.height: 32
                                    source: "qrc:/resources/images/icons/connect.svg"
                                    visible: modelData == accessRepeater.currentAccess

                                    anchors {
                                        right: parent.right
                                        rightMargin: 8
                                        verticalCenter: parent.verticalCenter
                                    }
                                }

                                Custom.HandMouseArea {
                                    onClicked: {
                                        popup.forceActiveFocus()
                                        accessRepeater.currentAccess = modelData
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumHeight: 88
                Layout.maximumHeight: 88
                Layout.fillWidth: true

                Item {
                    width: parent.width / 2 - 20
                    height: parent.height
                    anchors {
                        top: parent.top
                        topMargin: 4
                        left: parent.left
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
                    width: parent.width / 2 - 20
                    height: parent.height
                    anchors {
                        top: parent.top
                        topMargin: 4
                        right: parent.right
                    }

                    Custom.Button {
                        width: parent.width
                        text: tr.add
                        enabledCustom: installerValueText.selectedInstaller && accessRepeater.currentAccess
                        color: ui.colors.green1
                        anchors.centerIn: parent

                        onClicked: {
                            var settings = {
                                "facility_id": popup.facility.id,
                                "employee_id": installerValueText.selectedInstaller.employee_id
                            }

                            settings["permission"] = accessRepeater.currentAccess == "NO_ACCESS" ? ["READ"] : ["READ", "WRITE"]
                            settings["expiration_date_to_edit"] = accessRepeater.currentAccess

                            app.installers_module.save_employees_permission_for_facility(settings)
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

    Connections {
        target: app.employee_module

        onSearchInstallersSuccess: {
            popup.installersModel = installers
        }
    }

    Connections {
        target: app.installers_module

        onSaveEmployeesPermissionForFacilitySuccess: {
            popup.close()
        }
    }
}
