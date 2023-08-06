import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/"

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml" as Root

Rectangle {
    id: installersSettings

    property var devEnable: true
    property var sideMargin: 24
    property var privacyOfficerExists: false

    Connections {
        target: installersSettings

        onReRejectedEmails: {
            var resString;
            if (rejEm.length == 0) {
                resString = tr.specified_email_are_already_registered_on_a_hub
            } else {
                resString = util.insert(tr.pro_account_with_that_email_address_doesnt_exist, [rejEm[0]])
                for (var i = 0; i < rejEm.length-1; i++) {
                    resString = resString + "<br />" + rejEm[i+1]
                }
            }
            Popups.text_popup(tr.information, resString)
        }
    }

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: installersSettingsBar

        headerText: tr.installers_companies_menu_title
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: installersSettingsBar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: sideMargin
        contentEnabled: hub.current_user.user_permissions_update

        DS3.InfoContainer {
            anchors.horizontalCenter: parent.horizontalCenter

            imageType: DS3.InfoContainer.ImageType.PlugImage
            imageSource: "qrc:/resources/images/Athena/common_icons/EmptyInstallersImage.svg"
            descComponent.text: tr.add_first_user_pro
            visible: !usersView.count && !installationCompaniesView.item.visible
        }

        DS3.SettingsContainer {
            id: activeUsersContainer

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            title: tr.self_installers
            visible: usersView.count

            List {
                id: usersView

                width: parent.width
                height: contentHeight

                spacing: 1
                model: management.filtered_pro
                interactive: false

                delegate: Item {
                    width: usersView.width
                    height: 96

                    Loader {
                        id: userLoader

                        width: parent.width
                        height: 96

                        source: {
                            if (!user || index == -1) return ""
                            return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/InstallerDelegate.qml"
                        }
                    }
                    Component.onCompleted: {
                        if (user.privacy_access_settings) {
                            privacyOfficerExists = true
                        }
                    }
                }
            }
        }

        DS3.Spacing {
            height: usersView.count ? 24 : 0
        }

        Root.ContextLoader {
            id: installationCompaniesView

            width: parent.width
            height: item.height

            contextTarget: app.installationCompaniesView
        }

        Connections {
            target: installationCompaniesView.item

            onCompanyChoosen: (company) => companyInfoLoader.setSource(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/installers/CompanyInfo.qml",
                {companyData: company}
            )
        }

        DS3.Spacing {
            height: installationCompaniesView.item.visible ? 24 : 0
        }

        DS3.ButtonOutlined {
            id: inviteButton

            width: parent.width

            text: tr.invite_installer_company
            visible: hub.current_user.common_params_access && (!appUser.company_id || facility.data.company_id != "" || facility.id)

            onClicked: {
                Popups.popupByPath(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/installers/InviteInstallerOrCompanyPopup.qml"
                )
            }
        }
    }

    Loader {
        id: companyInfoLoader

        anchors.fill: parent
    }

    signal reRejectedEmails(variant rejEm)

    RejectedEmailsHandler {}
}