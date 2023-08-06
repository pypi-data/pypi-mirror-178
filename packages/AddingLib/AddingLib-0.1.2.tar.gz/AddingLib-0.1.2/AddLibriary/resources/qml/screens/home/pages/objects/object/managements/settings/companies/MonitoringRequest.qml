import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    id: monitoringRequestScreen

    property var sideMargin: 24
    property var email: null

    Connections {
        target: app

        onSearchedCompanies: {
            if (!response.companies.length) {
                companyNotFound.visible = true
                return
            }
            companyNotFound.visible = false
            inviteCompanyLoader.setSource(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/companies/AddingCompanies.qml",
                {
                    email: companyEmail.atomInput.text,
                    companies: response.companies
                }
            )
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    MouseArea {
        anchors.fill: parent
    }

    DS3.NavBarModal {
        id: monitoringRequestBar

        headerText: tr.invite_security_company
        isRound: false

        onClosed: () => {
            inviteCompanyLoader.setSource("")
        }
    }

    DS3.SettingsContainer {
        id: companyEmailItem

        width: parent.width - sideMargin * 2

        anchors {
            horizontalCenter: parent.horizontalCenter
            top: monitoringRequestBar.bottom
            topMargin: 24
        }

        DS3.InputSingleLine {
            id: companyEmail

            Connections {
                target: companyEmail.atomInput

                onTextChanged: {
                    companyNotFound.visible = false
                }
            }

            regex: ui.regexes.email
            hasValidationOnFocusLost: true

            validatorError: tr.invalid_email_format
            atomInput {
                label: tr.email
                placeholderText: tr.enter_company_email
                text: email ? email : ""
                maximumLength: 300
                required: false
            }
        }
    }

    DS3.SettingsContainer {
        width: parent.width - sideMargin * 2

        anchors {
            horizontalCenter: parent.horizontalCenter
            top: companyEmailItem.bottom
            topMargin: 24
        }

        DS3.CommentImportant {
            id: companyNotFound

            atomTitle {
                title: tr.invalid_email
                subtitle: tr.invalid_email_for_company_invitation_desktop
            }
            imageItem.source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"
            status: DS3.CommentImportant.Status.Attention
            visible: false
        }
    }

    DS3.ButtonBar {
        id: nextButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.next
        hasBackground: true
        enabled: companyEmail.atomInput.text.length

        button.onClicked: {
            if (!companyEmail.isValid) return

            companyNotFound.visible = false

            var settings = {
                "hub_hex_id": hub.hub_id,
                "email": companyEmail.atomInput.text
            }
            app.search_company(settings)
        }
    }
}