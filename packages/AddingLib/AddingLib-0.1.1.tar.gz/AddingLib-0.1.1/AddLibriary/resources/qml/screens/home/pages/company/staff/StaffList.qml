import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: staffBody
    color: companyStack.color

    Layout.fillWidth: true
    Layout.rightMargin: infoStaffComponent.visible ? 0 : 8
    Layout.alignment: Qt.AlignBottom | Qt.AlignLeft
    Layout.minimumHeight: {
        var height = staffLayout.height - panel.height - 1
//        if (height > scrollView.contentHeight) return scrollView.contentHeight
        return height
    }
    Layout.maximumHeight: Layout.minimumHeight

    property alias staffData: staffData

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true
        ScrollBar.horizontal.policy: {
            if (staffData.width > scrollView.width) {
                return ScrollBar.AlwaysOn
            }
            return ScrollBar.AlwaysOff
        }

        Flickable {
            contentWidth: staffData.width
            contentHeight: staffBody.height

            ListView {
                id: staffData

                width: headerItem.width
                height: parent.height

                boundsBehavior: Flickable.StopAtBounds
                headerPositioning: ListView.OverlayHeader

                model: appCompany.filtered_employees_model
                header: HeaderStaff {}
                populate: Transition {}

                ScrollBar.vertical: Custom.ScrollBar {
                    parent: scrollView
                    anchors {
                        top: parent.top
                        right: parent.right
                        bottom: parent.bottom
                    }

                    policy: {
                        if (staffData.contentHeight > staffData.height) {
                            return ScrollBar.AlwaysOn
                        }
                        return ScrollBar.AlwaysOff
                    }
                }
                Connections {
                    target: infoStaffComponent

                    onCurrentObjectChanged: {
                        if (!infoStaffComponent.currentObject) staff.ownCurrentIndex = -1
                    }
                }

                delegate: Item {
                    width: parent.width
                    height: 57
                    property var header: staffData.headerItem

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            ownCurrentIndex = index
                            infoStaffComponent.currentObject = employee
                        }
                    }

                    Custom.RoundedRect {
                        width: parent.width
                        height: parent.height - 1

                        radius: 10
                        color: ownCurrentIndex == index ? "transparent" : ui.colors.dark1
                        bottomRightCorner: ownCurrentIndex - index == 1
                        topRightCorner: {
                            if (ownCurrentIndex < 0) return false
                            return index - ownCurrentIndex == 1
                        }

                        RowLayout {
                            spacing: 4
                            anchors.fill: parent

                            Item {
                                id: nameItem

                                clip: true
                                Layout.minimumWidth: header.headerRow.children[1].width
                                Layout.maximumWidth: header.headerRow.children[1].width
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height

                                Custom.UserImage {
                                    id: avatarEmployeeList

                                    anchors {
                                        verticalCenter: parent.verticalCenter
                                        left: parent.left
                                        leftMargin: 8
                                    }

                                    width: 48

                                    imageSource: Object.keys(employee.photos).length !== 0 ? employee.photos["64x64"] : ""
                                    userName: employee.data.first_name + " " + employee.data.last_name
                                }

                                DS3.Text {
                                    width: parent.width - 16
                                    height: contentHeight

                                    anchors {
                                        verticalCenter: parent.verticalCenter
                                        left: parent.left
                                        leftMargin: 64
                                    }

                                    text: employee.data.first_name + " " + employee.data.last_name
                                    hasElide: true
                                }
                            }

                           Item {
                                id: roleItem

                                clip: true
                                Layout.minimumWidth: header.headerRow.children[3].width
                                Layout.maximumWidth: header.headerRow.children[3].width
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height

                                DS3.Text {
                                    id: rolesText

                                    width: parent.width

                                    anchors {
                                        verticalCenter: parent.verticalCenter
                                        left: parent.left
                                    }

                                    text: {
                                        var roles = app.roles_to_ui(
                                            appCompany.company_type == "MONITORING"
                                            ? util.remove_installers(employee.data.role.roles)
                                            : appCompany.company_type == "INSTALLATION"
                                            ? util.filter_installation_company_roles(employee.data.role.roles)
                                            : employee.data.role.roles
                                        )
                                        return roles.join(", ")
                                    }
                                    hasElide: true
                                }
                            }

                            Item {
                                id: phoneItem

                                clip: true
                                Layout.minimumWidth: header.headerRow.children[5].width
                                Layout.maximumWidth: header.headerRow.children[5].width
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height

                                DS3.Text {
                                    width: parent.width - 16
                                    height: contentHeight

                                    anchors.verticalCenter: parent.verticalCenter

                                    text: {
                                        if (!employee.data.phone_numbers.length) return tr.a911_unknown
                                        return employee.data.phone_numbers[0].number
                                    }
                                    hasElide: true
                                }
                            }
                            Item {
                                id: emailItem

                                clip: true
                                Layout.minimumWidth: header.headerRow.children[7].width
                                Layout.maximumWidth: header.headerRow.children[7].width
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height

                                DS3.Text {
                                    width: parent.width - 16
                                    height: contentHeight

                                    anchors.verticalCenter: parent.verticalCenter

                                    text: employee.data.email
                                    hasElide: true
                                }
                            }

                            Item {
                                id: toggleItem
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height
                                Layout.minimumWidth: header.headerRow.children[9].width
                                Layout.maximumWidth: header.headerRow.children[9].width

                                Item {
                                    anchors.fill: parent

                                    Rectangle {
                                        width: 1
                                        height: parent.height - 24

                                        anchors {
                                            verticalCenter: parent.verticalCenter
                                            left: parent.left
                                        }

                                        color: companyStack.color
                                    }

                                    Custom.Toggle {
                                        checked: employee.data.status == "ACTIVE"
                                        enabled: appUser.employee_id != employee.id
                                            && companyAccessAPI.canEditEmployee(JSON.stringify(employee.data.role.roles))
                                        anchors {
                                            centerIn: parent
                                            horizontalCenterOffset: 5
                                        }

                                        mouseArea.onClicked: {
                                            var data = {"id": employee.id, "active": !checked}
                                            app.employee_module.set_employee_status(data)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            Custom.RoundedRect {
                height: parent.height - staffData.contentHeight

                anchors {
                   left: parent.left
                   right: parent.right
                   bottom: parent.bottom
                }

                color: ui.colors.dark3
                radius: 10

                Custom.EmptySpaceLogo {
                    visible: staffList.staffData.model.length == 0
                }

                topRightCorner: {
                    if (appCompany.filtered_employees_model.length == 0 || ownCurrentIndex == -1) return false
                    return ownCurrentIndex == appCompany.filtered_employees_model.length - 1
                }
            }
        }
    }
}