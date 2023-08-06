import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    id: companiesSettings

    property var sideMargin: 24

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: companiesSettingsBar

        headerText: tr.security_companies
        showCloseIcon: false
        isRound: false
    }

    DS3.InputSearch {
        id: searchField

        Component.onDestruction: {
            management.companies.filtered.set_text("")
        }

        width: parent.width

        anchors.top: companiesSettingsBar.bottom

        placeholder: tr.search_location
        withSpinner: true
        find: () => {
            management.companies.filtered.set_text(atomInput.text)
        }
    }

    DS3.SettingsPickerImage {
        id: countriesField

        width: parent.width

        Connections {
            target: management.companies

            onCompaniesReceived: {
                var data = management.companies.get_countries(tr.get_selected())

                countriesField.model = data.countries.map((country, idx) => {
                    return {
                        text: country,
                        image: idx == 0
                            ? "qrc:/resources/images/desktop/countries/earth.png"
                            : "qrc:/resources/images/desktop/countries/" + data.codes[idx] + ".png"
                        }
                    }
                )
            }
        }

        onCurrentIndexChanged: {
            management.companies.filtered.set_country(management.companies.get_countries(tr.get_selected()).codes[countriesField.currentIndex])
        }

        anchors {
            top: searchField.bottom
            topMargin: 1
        }

        backgroundColor: ui.ds3.bg.high
    }

    DS3.InfoContainer {
        anchors {
            top: countriesField.bottom
            topMargin: 24
            horizontalCenter: parent.horizontalCenter
        }

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/fibra/NotFound-XL.svg"
        titleComponent.text: tr.no_security_company_now
        descComponent.text: tr.no_security_company_now_desc
        visible: !management.companies.filtered.length
    }

    DS3.ListView {
        id: companiesListView

        anchors {
            top: countriesField.bottom
            bottom: inviteCompany.top
            left: parent.left
            right: parent.right
        }

        list {
            spacing: 4
            model: management.companies.filtered
            header: Item {
                width: parent.width
                height: (visible ? noSecurityCompanyYet.height + companiesListView.contentPadding : 0) + companiesListView.contentPadding

                visible: management.companies.company_alert && management.companies.filtered.length

                DS3.SettingsContainer {
                    id: noSecurityCompanyYet

                    width: parent.width

                    anchors.verticalCenter: parent.verticalCenter

                    DS3.CommentImportant {
                        id: noSecurityCompanyYetComment

                        atomTitle.title: tr.you_havent_selected_a_security_company_yet
                        imageItem.source: "qrc:/resources/images/Athena/notifications/ShieldQuestion-M.svg"
                    }
                }
            }
            delegate: Item {
                id: delegate

                width: parent.width
                height: childrenRect.height + (
                    delegate.ListView.nextSection != delegate.ListView.section && delegate.ListView.nextSection ? 24 : 0
                )

                DS3.SettingsContainer {
                    width: parent.width

                    anchors.horizontalCenter: parent.horizontalCenter

                    CompanyDelegate {}
                }
            }

            section.property: "company_monitoring"
            section.labelPositioning: ViewSection.InlineLabels
            section.criteria: ViewSection.FullString
            section.delegate: Column {
                width: parent.width

                DS3.Text {
                    text: {
                        if (section == "APPROVED") return tr.companies
                        if (section == "PENDING_APPROVAL") return tr.pending_subscribe_requests
                        if (section == "PENDING_REMOVAL") return tr.pending_unsubscribe_requests
                        return tr.available_companies
                    }
                    style: ui.ds3.text.special.SectionCaps
                    color: ui.ds3.figure.secondary
                }
            }
        }
    }

    DS3.ButtonBar {
        id: inviteCompany

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.invite_company_by_email
        hasBackground: true
        visible: !appUser.company_id || (appUser.company_id && management && management.devices && management.devices.hub && management.devices.hub.current_user.common_params_access && management.facility_access)
        iconSource: "qrc:/resources/images/Athena/common_icons/Envelope-S.svg"

        button.onClicked: {
            inviteCompanyLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/companies/MonitoringRequest.qml")
        }
    }

    Custom.BlockLoading {
        minTime: 1000
        customOpacity: 0.2
        startSignals: [management.companies.companiesLoad]
        stopSignals: [management.companies.companiesReceived, management.companies.companiesNotReceived]

        Component.onCompleted: {
            app.get_companies(management, {"hub_id": hub.hub_id})
        }
    }

    Loader {
        id: companyViewLoader

        anchors.fill: parent
    }

    Loader {
        id: inviteCompanyLoader

        anchors.fill: parent
    }
}
