import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups

Rectangle {
    id: addingCompaniesScreen

    property var sideMargin: 24
    property var email: null
    property var companies: null
    property var selectedCompany: companies[0].data

    Connections {
        target: app

        onActionFailed: {
            inviteCompanyLoader.setSource("")
        }

        onActionSuccess: {
            inviteCompanyLoader.setSource("")
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    MouseArea {
        anchors.fill: parent
    }

    DS3.NavBarModal {
        id: addingCompaniesBar

        headerText: tr.invite_security_company
        isRound: false
        showBackArrow: true

        onBackAreaClicked: {
            inviteCompanyLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/companies/MonitoringRequest.qml", {email: email})
        }

        onClosed: () => {
            inviteCompanyLoader.setSource("")
        }
    }

    DS3.ScrollView {
        id: scrollView

        anchors {
            fill: undefined
            top: addingCompaniesBar.bottom
            bottom: inviteButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.Text {
            width: parent.width

            text: companies.length > 1 ? tr.choose_company_desc : tr.invite_security_company_desc
            style: ui.ds3.text.title.SBold
            horizontalAlignment: Text.AlignHCenter
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            Item {
                width: parent.width
                height: companiesListView.contentHeight

                ListView {
                    id: companiesListView

                    anchors.fill: parent

                    clip: true
                    spacing: 1
                    boundsBehavior: Flickable.StopAtBounds
                    model: companies

                    delegate: DS3.CompanySelection {
                        companyName.text: modelData.data.name
                        companyImage.source: modelData.data.logo_url
                        objectName: "delegate"
                        checked: index == 0
                        companyChecked: () => {
                            let availableCompanies = companiesListView.contentItem.children

                            if (!availableCompanies.length) return false
                            for (var index in availableCompanies) {
                                if (availableCompanies[index].objectName == "delegate") {
                                    availableCompanies[index].checked = false
                                }
                            }
                            checked = true
                            selectedCompany = modelData.data
                        }
                    }
                }
            }
        }
    }

    DS3.ButtonBar {
        id: inviteButton

        property var monitoringStatus: selectedCompany ? selectedCompany.monitoring_status : null

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: {
            if (!monitoringStatus) return tr.send_monitoring_start_request

            if (monitoringStatus == "PENDING_APPROVAL") return tr.refuse_from_monitoring
            if (monitoringStatus == "APPROVED") return tr.refuse_from_monitoring
            if (monitoringStatus == "PENDING_REMOVAL") return tr.send_monitoring_undo_remove_request

            return tr.send_monitoring_start_request
        }
        button.isAttention: {
            if (!monitoringStatus) return false

            if (monitoringStatus == "PENDING_APPROVAL") return true
            if (monitoringStatus == "APPROVED") return true
            if (monitoringStatus == "PENDING_REMOVAL") return false

            return false
        }
        hasBackground: true
        enabled: !!selectedCompany
        isOutline: button.isAttention

        button.onClicked: {
            if (monitoringStatus == "PENDING_APPROVAL") {
                app.hub_management_module.delete_security_company_binding(selectedCompany.id)
                return
            }

            if (monitoringStatus == "APPROVED") {
                app.hub_management_module.delete_security_company_binding(selectedCompany.id)
                return
            }

            if (monitoringStatus == "PENDING_REMOVAL") {
                function todo() {
                    app.hub_management_module.cancel_delete_security_company_binding(selectedCompany.id)
                }
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        text: tr.send_monitoring_undo_remove_request_info,
                        firstButtonText: tr.confirm,
                        secondButtonText: tr.cancel,
                        firstButtonCallback: todo
                    }
                )
                return
            }

            app.hub_management_module.create_security_company_binding(selectedCompany.id)
        }
    }
}