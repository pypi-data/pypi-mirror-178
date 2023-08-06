import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: companyViewScreen

    property var currentCompany: null
    property var currentCompanyState: null
    property var sideMargin: 24

    Custom.BlockLoading {
        minTime: 1000
        customOpacity: 0.2
        startSignals: [management.companies.companyLoad]
        stopSignals: [management.companies.companyReceived, management.companies.companyNotReceived]

        Component.onCompleted: {
            app.get_company(management, {"hub_id": hub.hub_id, "company_id": currentCompany.id})
        }
    }

    Connections {
        target: management.companies

        onCompanyReceived: {
            if (currentCompany.id == companyData.id) {
                currentCompany = companyData
                currentCompanyState = companyData.monitoring_status
            }
        }

        onCompanyStateChanged: {
            if (currentCompany.id == companyId) {
                currentCompanyState = companyState
            }
        }
    }

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id:  companyViewBar

        headerText: currentCompany.name
        showCloseIcon: false
        isRound: false
        showBackArrow: true

        onBackAreaClicked: {
            companyViewLoader.source = ""
        }
    }

    DS3.ScrollView {
        id: scrollView

        anchors {
            fill: undefined
            top: companyViewBar.bottom
            bottom: bottomButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.CompanyImage {
            width: 136
            height: 136

            anchors.horizontalCenter: parent.horizontalCenter

            source: currentCompany.logo_url
            name: currentCompany.name
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            Repeater {
                model: currentCompany.contacts ? currentCompany.contacts : []

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: modelData.description ? modelData.description : tr.company_phone_number
                    atomTitle.subtitle: modelData.phone_number ? modelData.phone_number : ""
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"

                    onRightControlClicked: {
                        util.set_clipboard_text(atomTitle.subtitle)
                    }
                }
            }

            Repeater {
                model: currentCompany.customer_inquiries_emails ? currentCompany.customer_inquiries_emails : []

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: tr.email
                    atomTitle.subtitle: modelData ? modelData : ""
                    visible: !!atomTitle.subtitle
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/Shape-M.svg"
                    buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"

                    onRightControlClicked: {
                        util.set_clipboard_text(atomTitle.subtitle)
                    }
                }
            }

            DS3.InfoTitleButtonIcon {
                atomTitle.title: tr.website
                atomTitle.subtitle: currentCompany.web_site_url ? currentCompany.web_site_url : ""
                visible: !!atomTitle.subtitle
                leftIcon.source: "qrc:/resources/images/Athena/common_icons/Connection-M.svg"
                buttonIcon.source: "qrc:/resources/images/Athena/common_icons/ExternalLink-M.svg"

                onRightControlClicked: {
                    Qt.openUrlExternally(atomTitle.subtitle)
                }
            }
        }

        DS3.Spacing {
            height: !!currentCompany.locationsString ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.available_in_alt + ":"
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: !!currentCompany.locationsString
        }

        DS3.Spacing {
            height: !!currentCompany.locationsString ? 4 : 0
        }
        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InfoTitle {
                width: parent.width

                atomTitle.title: currentCompany.locationsString ? currentCompany.locationsString : ""
                visible: !!currentCompany.locationsString
            }
        }

        DS3.InfoFooter {
            visible: !!subtitleUpper.text
            footerType: DS3.InfoFooter.FooterType.User
            subtitleUpper.text: {
                const userObject = management.users.get_user(currentCompany.id)
                if (userObject) return `${tr.company_id} ${userObject.index}`
                return ""
            }
        }
    }

    DS3.ButtonBar {
        id: bottomButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: {
            return {
                "PENDING_REMOVAL": tr.send_monitoring_undo_remove_request,
                "NO_STATE": tr.send_monitoring_start_request,
                "APPROVED": tr.refuse_from_monitoring,
                "PENDING_APPROVAL": tr.refuse_from_monitoring
            }[currentCompanyState]
        }

        hasBackground: true
        visible: !appUser.company_id || (appUser.company_id && management && management.devices && management.devices.hub && management.devices.hub.current_user.common_params_access && management.facility_access)
        button.color: {
            return currentCompanyState ? {
                "PENDING_APPROVAL": ui.ds3.figure.attention,
                "PENDING_REMOVAL": ui.ds3.figure.interactive,
                "APPROVED": ui.ds3.figure.attention,
                "NO_STATE": ui.ds3.figure.interactive
            }[currentCompanyState]
            :
            ui.ds3.figure.interactive
        }

        isOutline: button.color == ui.ds3.figure.attention

        button.onClicked: {
            if (currentCompanyState == "APPROVED") {
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.warning,
                        text: tr.you_are_about_to_send_the_request_to_the_security_company,
                        firstButtonText: tr.yes,
                        secondButtonText: tr.cancel,
                        firstButtonCallback: () => {
                            app.hub_management_module.delete_security_company_binding(companyViewScreen.currentCompany.id)
                        }
                    }
                )
            }
            else if (currentCompanyState == "PENDING_REMOVAL") {
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        text: tr.send_monitoring_undo_remove_request_info,
                        firstButtonText: tr.confirm,
                        secondButtonText: tr.cancel,
                        firstButtonCallback: () => {
                            app.hub_management_module.cancel_delete_security_company_binding(companyViewScreen.currentCompany.id)
                        }
                    }
                )
            }
            else if (currentCompanyState == "PENDING_APPROVAL") {
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.warning,
                        text: tr.you_are_about_to_send_the_request_to_the_security_company,
                        firstButtonText: tr.yes,
                        secondButtonText: tr.cancel,
                        firstButtonCallback: () => {
                            app.hub_management_module.delete_security_company_binding(companyViewScreen.currentCompany.id)
                        }
                    }
                )
            }
            else if (currentCompanyState == "NO_STATE") {
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.warning,
                        text: tr.you_are_about_to_send_the_request_to_the_security_company,
                        firstButtonText: tr.yes,
                        secondButtonText: tr.cancel,
                        firstButtonCallback: () => {
                            app.hub_management_module.create_security_company_binding(companyViewScreen.currentCompany.id)
                        }
                    }
                )
            }
        }
    }
}
