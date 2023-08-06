import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom



Column {
    id: roleItem
    property var roles: new Set([])
    property var delegateWidth: 0
    property var seniorCMSEngineerAdjustmentAllowed: false

//    property var uiRolesAlt: {
//        "OWNER": tr.owner_911,
//        "SENIOR_CMS_ENGINEER": tr.a911_Senior_monitoring_station_engineer,
//        "CMS_ENGINEER": tr.a911_monitoring_station_engineer,
//        "HEAD_OF_INSTALLERS": tr.a911_head_of_installers,
//        "INSTALLER": tr.a911_installer,
//        "HEAD_OF_OPERATORS": tr.a911_head_of_operators,
//        "OPERATOR": tr.a911_operator,
//        "RAPID_RESPONSE_TEAM": tr.a911_gbr,
//        "PRO": "PRO"
//    }

    property var uiRoles: {
        let roles = isOwner ? {"OWNER": tr.owner_911} : {}
        if (appCompany.data.provided_services.monitoring && appCompany.data.provided_services.installation)  {
            return Object.assign(roles, {
                "SENIOR_CMS_ENGINEER": tr.a911_Senior_monitoring_station_engineer,
                "CMS_ENGINEER": tr.a911_monitoring_station_engineer,
                "HEAD_OF_INSTALLERS": tr.a911_head_of_installers,
                "INSTALLER": tr.a911_installer,
                "HEAD_OF_OPERATORS": tr.a911_head_of_operators,
                "OPERATOR": tr.a911_operator,
            })
        } else if (appCompany.data.provided_services.installation) {
            return Object.assign(roles, {
                "HEAD_OF_INSTALLERS": tr.a911_head_of_installers,
                "INSTALLER": tr.a911_installer,
            })
        } else if (appCompany.data.provided_services.monitoring) {
            return Object.assign(roles, {
                "SENIOR_CMS_ENGINEER": tr.a911_Senior_monitoring_station_engineer,
                "CMS_ENGINEER": tr.a911_monitoring_station_engineer,
                "HEAD_OF_OPERATORS": tr.a911_head_of_operators,
                "OPERATOR": tr.a911_operator,
            })
        }
    }

    property var keys: Object.keys(uiRoles)
    property var isOwner: false
    property var isSeniorCMS: false
    property var isSelf: currentObject && appUser.employee_id == currentObject.id
    property var isMix: appCompany.data.provided_services.monitoring && appCompany.data.provided_services.installation
    property var isInstallation: !isMix && appCompany.data.provided_services.installation

    property var rolesSize: null

    enabled: !currentObject || !isSelf || isOwner || isSeniorCMS

    width: parent.width
    spacing: 8

    Repeater {
        id: companyRoles
        model: Object.values(uiRoles)
        anchors.horizontalCenter: parent.horizontalCenter

        delegate: Rectangle {
            id: selectCompany

            width: delegateWidth != 0 ? delegateWidth: parent.width
            height: 48

            color: ui.colors.dark1
            radius: 10
            opacity: enabled ? 1 : 0.6
            enabled: isEnabled()
            anchors{
                horizontalCenter: parent.horizontalCenter
            }

            visible: {
                var targetRole = keys[companyRoles.model.indexOf(modelData)]
                return isOwner || isSeniorCMS || (
                    isSelf ?
                        appUser.role.includes(targetRole) :
                        companyAccessAPI.canEditEmployee(
                            JSON.stringify([targetRole])
                        )
                )
            }

            function isEnabled() {
                let curRole = keys[companyRoles.model.indexOf(modelData)]
                return !(
                    (
                        // Only OWNER can see such role. This role cannot be removed
                        curRole == "OWNER"
                    ) || (
                        // If you want promote employee to HEAD_OF_INSTALLERS, you can not disable INSTALLER role for him
                        curRole == "INSTALLER"
                        && roles.has("HEAD_OF_INSTALLERS")
                    ) || (
                        // If you want promote employee to SENIOR_CMS_ENGINEER, you can not disable CMS_ENGINEER role for him
                        curRole == "CMS_ENGINEER"
                        && roles.has("SENIOR_CMS_ENGINEER")
                    ) || (
                        // If you want promote employee to HEAD_OF_OPERATORS, you can not disable OPERATOR role for him
                        curRole == "OPERATOR"
                        && roles.has("HEAD_OF_OPERATORS")
                    ) || (
                        // If you want promote employee to SENIOR_CMS_ENGINEER, you can not disable any other role for him
                        curRole != "SENIOR_CMS_ENGINEER"
                        && roles.has("SENIOR_CMS_ENGINEER")
                        && !isSelf
                        && !seniorCMSEngineerAdjustmentAllowed
                    ) || (
                        // If you are SENIOR_CMS_ENGINEER, you cannot disable this role for yourself
                        // except the case you are OWNER
                        curRole == "SENIOR_CMS_ENGINEER"
                        && isSelf
                        && !isOwner
                    )
                )
            }

            Connections {
                target: roleItem

                onRolesChanged: {
                    badgeImage.source = roles.has(keys[companyRoles.model.indexOf(modelData)]) ? "qrc:/resources/images/icons/a-selected-bage-green.svg" : "qrc:/resources/images/icons/a-unselected-badge.svg"
                    selectCompany.enabled = isEnabled()
                }
            }

            Custom.FontText {
                width: parent.width - 44
                height: contentHeight
                text: modelData
                color: ui.colors.light3
                elide: Text.ElideRight
                anchors {
                    left: parent.left
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }
            }

            Image {
                id: badgeImage

                sourceSize.width: 32
                sourceSize.height: 32
                source: roles.has(keys[companyRoles.model.indexOf(modelData)]) ? "qrc:/resources/images/icons/a-selected-bage-green.svg" : "qrc:/resources/images/icons/a-unselected-badge.svg"

                Connections {
                    target: roleItem
                }

                anchors {
                    right: parent.right
                    rightMargin: 8
                    verticalCenter: parent.verticalCenter
                }
            }

            Custom.HandMouseArea {
                id: delegArea
                anchors.fill: parent

                onClicked: {
                    if (badgeImage.source != "qrc:/resources/images/icons/a-selected-bage-green.svg") {
                        badgeImage.source = "qrc:/resources/images/icons/a-selected-bage-green.svg"
                        roles.add(keys[companyRoles.model.indexOf(modelData)])

                        if (keys[companyRoles.model.indexOf(modelData)] == "HEAD_OF_OPERATORS") {
                            roles.add("OPERATOR")
                        }

                        if (keys[companyRoles.model.indexOf(modelData)] == "SENIOR_CMS_ENGINEER") {
                            roles.add("CMS_ENGINEER")
                            if (!isOwner || !isSelf) Object.keys(uiRoles).forEach((role) => roles.add(role))
                        }

                        if (keys[companyRoles.model.indexOf(modelData)] == "HEAD_OF_INSTALLERS") {
                            roles.add("INSTALLER")
                        }
                    }
                    else {
                        badgeImage.source = "qrc:/resources/images/icons/a-unselected-badge.svg"
                        roles.delete(keys[companyRoles.model.indexOf(modelData)])

                        if (keys[companyRoles.model.indexOf(modelData)] == "HEAD_OF_OPERATORS") {
                            roles.delete("OPERATOR")
                        }

                        if (keys[companyRoles.model.indexOf(modelData)] == "SENIOR_CMS_ENGINEER") {
                            roles.delete("CMS_ENGINEER")
                            if (!isOwner || !isSelf) Object.keys(uiRoles).forEach((role) => roles.delete(role))
                        }

                        if (keys[companyRoles.model.indexOf(modelData)] == "HEAD_OF_INSTALLERS") {
                            roles.delete("INSTALLER")
                        }
                    }

                    rolesSize = roles.size
                    rolesChanged()
                }
            }
        }
    }
}