import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: backgroundRect

    color: ui.colors.black
    anchors.fill: parent

    Item {
        id: backItem

        width: parent.width
        height: 50
        anchors.top: parent.top

        Image {
            id: backImage

            sourceSize.width: 24
            sourceSize.height: 24
            source: "qrc:/resources/images/icons/back.svg"
            anchors {
                left: parent.left
                leftMargin: 16
                verticalCenter: parent.verticalCenter
            }

            Custom.HandMouseArea {
                onClicked: {
                    pageLoader.setSource("")
                }
            }
        }

        Custom.FontText {
            width: 216
            height: contentHeight
            text: tr.a911_choose_company
            color: ui.colors.light3
            elide: Text.ElideRight

            anchors {
                left: backImage.right
                leftMargin: 16
                verticalCenter: parent.verticalCenter
            }
        }
    }

    ScrollView {
        id: scrollView

        width: parent.width
        clip: true
        anchors.top: backItem.bottom
        anchors.bottom: parent.bottom

        Column {
            width: scrollView.width
            spacing: 8

            // User companies
            Repeater {

                model: appUser.accepted_companies

                delegate: Rectangle {
                    id: currentCompany

                    property var userCompanies: modelData
                    width: backgroundRect.width - 16
                    height: {
                        return 16 + companyItem.height + 16 + modelData.role.length * 48 + 8;
                    }

                    color: ui.colors.dark3
                    radius: 10
                    anchors.horizontalCenter: parent.horizontalCenter

                    Item {
                        id: companyItem

                        width: parent.width
                        height: companyName.height > companyLogo.height ? companyName.height : companyLogo.height
                        anchors {
                            top: parent.top
                            topMargin: 16
                        }

                        Custom.UserImage {
                            id: companyLogo

                            width: 42
                            height: 42
                            userName: modelData.role.includes("PRO") ? tr.a911_privat_account : modelData.company_name
                            imageSource: {
                                if (modelData.role.includes("PRO")) return "qrc:/resources/images/icons/a-logo-pro.svg"
                                if (!modelData.company_logo.image_id) return ""
                                return util.get_image_with_resolution(modelData.company_logo.images, "64x64")
                            }
                            anchors {
                                top: parent.top
                                left: parent.left
                                leftMargin: 12
                            }
                        }

                        Custom.FontText {
                            id: companyName

                            width: 210
                            height: contentHeight
                            text: modelData.role.includes("PRO") ? tr.a911_privat_account : modelData.company_name
                            color: ui.colors.light4
                            maximumLineCount: 3
                            wrapMode: Text.Wrap
                            elide: Text.ElideRight

                            anchors {
                                left: companyLogo.right
                                leftMargin: 12
                                verticalCenter: companyLogo.verticalCenter
                            }
                        }
                    }

                    // Company Roles
                    Column {
                        width: currentCompany.width
                        spacing: 8
                        anchors {
                            top: companyItem.bottom
                            topMargin: 16
                        }

                        Repeater {
                            id: companyRoles

                            model: modelData.role

                            delegate: Rectangle {
                                id: selectCompany

                                width: parent.width - 24
                                height: 40
                                color: ui.colors.dark1
                                radius: 10
                                anchors{
                                    horizontalCenter: parent.horizontalCenter
                                }

                                Custom.FontText {
                                    width: parent.width - 44
                                    height: contentHeight
                                    text: popup.uiRoles[modelData]
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
                                    source: {
                                        if (!appUser.company_id && modelData == "PRO") {
                                            return "qrc:/resources/images/icons/a-selected-bage-green.svg"
                                        }
                                        if (modelData == "PRO") return "qrc:/resources/images/icons/a-unselected-badge.svg"
                                        return (userCompanies.company_id == appUser.company_id && appUser.role.includes(modelData)) ? "qrc:/resources/images/icons/a-selected-bage-green.svg" : "qrc:/resources/images/icons/a-unselected-badge.svg"
                                    }

                                    anchors {
                                        right: parent.right
                                        rightMargin: 8
                                        verticalCenter: parent.verticalCenter
                                    }
                                }

                                Custom.HandMouseArea {
                                    anchors.fill: parent

                                    onClicked: {
                                        if (badgeImage.source != "qrc:/resources/images/icons/a-unselected-badge.svg") return
                                        if (modelData == "PRO") {
                                            application.debug("user popup -> change company -> login as PRO")
                                            app.login_module.login_into_personal_account()
                                        } else {
                                            application.debug("user popup -> change company -> login as " + modelData + " into `" + userCompanies.company_name + "` (" + userCompanies.company_id + ")", false)
                                            __ga__.report("activity", "user popup -> change company -> login into COMPANY")
                                            app.login_module.login_into_company(userCompanies.company_id, modelData)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Item {
                width: parent.width
                height: 8
            }
        }
    }
}
