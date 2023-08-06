import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: popup

//  Result on search by email
    property var searchResult

    width: 500
    height: 500

    defaultHeaderBackgroundColor: ui.ds3.bg.high
    enterOrReturnedPressedCallback: () => footerItem.enabled && footerItem.button.clicked()
    backspacePressedCallback: () => searchResult = null

    onOpened: input.atomInput.forceActiveFocus()

    Connections {
        target: app.hub_management_module

        onSearchInstallersResultReceived: (searchResult) => popup.searchResult = searchResult
    }

    header: DS3.NavBarModal {
        headerText: tr.invite_installer_company_title
        showBackArrow: chooseCompanyOrPro.visible

        onBackAreaClicked: searchResult = null
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        visible: !chooseCompanyOrPro.visible

        width: parent.width

        DS3.InputSingleLine {
            id: input

            regex: ui.regexes.email
            hasValidationOnFocusLost: true
            validatorError: tr.incorrect_email_format_911
            atomInput {
                label: tr.email
                placeholderText: tr.email_tip_installer
            }

            onVisibleChanged: {
                if (visible) atomInput.forceActiveFocus()
                else input.forceActiveFocus()
            }
        }
    }

    Column {
        width: parent.width

        visible: !chooseCompanyOrPro.visible && !!searchResult

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.CommentImportant {
                atomTitle {
                    title: tr.no_installers_found_title
                    subtitle: tr.invalid_email_for_company_invitation_desktop
                }
                imageItem.source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"
                status: DS3.CommentImportant.Status.Attention
            }
        }
    }

    Column {
        id: chooseCompanyOrPro

//      Selected pro or company. One of "PRO", "COMPANY"
        property var selectedType

        width: parent.width

        spacing: 24
        visible: !!popup.searchResult && (!!proPart.proData || !!companyPart.companyData)

        Column {
            id: proPart

            readonly property var proData: !!popup.searchResult
                && !!popup.searchResult.installers && popup.searchResult.installers[0]

            width: parent.width

            visible: !!proData

            DS3.TitleSection {
                width: parent.width

                isBgTransparent: true
                isCaps: true
                text: tr.self_installer
                forceTextToLeft: true
            }

            DS3.SettingsContainer {
                width: parent.width

                DS3.UserSelectionSingle {
                    id: selectionPro

                    property var userImageUrls: !!proPart.proData && proPart.proData.image_urls || ({
                        base_path: '',
                        small: ''
                    })

                    width: parent.width

                    imageSource: `${userImageUrls.base_path}${userImageUrls.small}`
                    atomTitle {
                        title: !!proPart.proData
                        ? `${proPart.proData.first_name} ${proPart.proData.last_name}`
                        : ""
                    }
                    role: tr.pro
                    selected: chooseCompanyOrPro.selectedType == "PRO"

                    onSelectedCallback: () => chooseCompanyOrPro.selectedType = "PRO"
                }
            }
        }

        Column {
            id: companyPart

            readonly property var companyData: !!popup.searchResult
                && !!popup.searchResult.companies && popup.searchResult.companies[0]

            width: parent.width

            visible: !!companyData

            DS3.TitleSection {
                width: parent.width

                isBgTransparent: true
                isCaps: true
                text: tr.installation_company
                forceTextToLeft: true
            }

            DS3.SettingsContainer {
                width: parent.width

                DS3.CompanySelectionSingle {
                    id: selectionCompany

                    width: parent.width

                    companyName.text: companyPart.companyData ? companyPart.companyData.name : ""
                    companyImage.source: companyPart.companyData ? companyPart.companyData.logo_url : ""
                    selected: chooseCompanyOrPro.selectedType == "COMPANY"

                    onSelectedCallback: () => chooseCompanyOrPro.selectedType = "COMPANY"
                }
            }
        }
    }

    footer: DS3.ButtonBar {
        enabled: chooseCompanyOrPro.visible ? !!chooseCompanyOrPro.selectedType : true
        hasBackground: true
        buttonText: chooseCompanyOrPro.visible ? tr.invite_button : tr.next

        button.onClicked: {
            if (!chooseCompanyOrPro.visible) {
                if (input.checkValid())
                    app.hub_management_module.search_installers_and_companies(input.atomInput.text)
            } else {
                if (chooseCompanyOrPro.selectedType == "PRO")
                    app.hub_management_module.invite_users(hub, [input.atomInput.text], true)
                else
                    app.hub_management_module.invite_installation_company(companyPart.companyData.company_hex_id, hub.id)
                popup.close()
            }
        }
    }
}