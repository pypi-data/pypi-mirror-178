import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: companyFoundScreen

    property var companies: null
    property var companyName: ""
    property var countryCode: ""

    Item {
        id: foundScreenHeader

        width: parent.width * 0.5
        height: foundScreenHeaderItem.height

        anchors {
            top: parent.top
            topMargin: 48
            horizontalCenter: parent.horizontalCenter
        }

        Item {
            id: foundScreenHeaderItem

            width: parent.width
            height: foundScreenHeaderText.contentHeight

            Desktop.NormalText {
                id: foundScreenHeaderText

                text: tr.company_creation_title
                color: ui.colors.light3
                size: 32
                bold: true

                anchors.fill: parent
            }
        }
    }

    Item {
        id: foundScreenSubHeader

        width: parent.width * 0.5
        height: foundScreenSubHeaderItem.height

        anchors {
            top: foundScreenHeader.bottom
            topMargin: 32
            horizontalCenter: parent.horizontalCenter
        }

        Item {
            id: foundScreenSubHeaderItem

            width: parent.width
            height: foundScreenSubHeaderText.contentHeight

            Desktop.NormalText {
                id: foundScreenSubHeaderText

                text: tr.company_search_merge_title
                color: ui.colors.light3
                size: 24
                bold: true

                anchors.fill: parent
            }
        }
    }

    Item {
        id: foundScreenList

        width: parent.width * 0.5

        anchors {
            top: foundScreenSubHeader.bottom
            topMargin: 40
            horizontalCenter: parent.horizontalCenter
            bottom: foundScreenCreate.top
            bottomMargin: 48
        }

        ScrollView {
            id: scrollView

            clip: true
            width: parent.width

            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            ScrollBar.vertical.policy: {
                if (scrollView.contentHeight > scrollView.height) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }

            Column {
                spacing: 16
                width: foundScreenList.width

                Item {
                    id: foundScreenTipItem

                    width: parent.width - 24
                    height: foundScreenTipText.contentHeight

                    visible: foundedCompaniesColumn.visible

                    Desktop.NormalText {
                        id: foundScreenTipText

                        text: tr.company_search_merge_description
                        color: ui.colors.middle1

                        anchors.fill: parent
                    }
                }

                Item {
                    width: parent.width - 24
                    height: 4

                    visible: foundedCompaniesColumn.visible
                }

                Column {
                    id: foundedCompaniesColumn

                    spacing: 24
                    width: foundScreenList.width - 24
                    visible: foundedCompanies.model.length > 0

                    Repeater {
                        id: foundedCompanies

                        model: companyFoundScreen.companies ? companyFoundScreen.companies.availableCompanies : []

                        delegate: Desktop.CompanyDelegate {
                            currentCompany: modelData
                        }
                    }
                }

                Item {
                    width: parent.width - 24
                    height: 16

                    visible: notFoundedCompaniesColumn.visible
                }

                Item {
                    id: notFoundScreenTipItem

                    width: parent.width - 24
                    height: notFoundScreenTipText.contentHeight

                    visible: notFoundedCompaniesColumn.visible

                    Desktop.NormalText {
                        id: notFoundScreenTipText

                        text: tr.company_search_blurr_description
                        color: ui.colors.middle1

                        anchors.fill: parent
                    }
                }

                Item {
                    width: parent.width - 24
                    height: 4

                    visible: notFoundedCompaniesColumn.visible
                }

                Column {
                    id: notFoundedCompaniesColumn

                    spacing: 24
                    width: foundScreenList.width - 24
                    visible: notFoundedCompanies.model.length > 0

                    Repeater {
                        id: notFoundedCompanies

                        model: companyFoundScreen.companies ? companyFoundScreen.companies.notAvailableCompanies : []

                        delegate: Desktop.CompanyDelegate {
                            currentCompany: modelData
                        }
                    }
                }
            }
        }
    }

    Item {
        id: foundScreenCreate

        width: parent.width * 0.5
        height: foundScreenCreateTip.height + 16 + 48

        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
            bottomMargin: 32
        }

        Item {
            id: foundScreenCreateTip

            width: parent.width
            height: foundScreenCreateText.contentHeight

            Desktop.NormalText {
                id: foundScreenCreateText

                text: tr.company_search_not_found_company
                size: 24
                bold: true
                color: ui.colors.light3

                anchors.fill: parent
            }
        }

        Item {
            width: foundScreenCreateButton.textButton.contentWidth + 64
            height: 48

            anchors {
                left: parent.left
                bottom: parent.bottom
            }

            Custom.Button {
                id: foundScreenCreateButton

                width: parent.width
                text: tr.button_create_company_new
                textButton.textFormat: Text.PlainText

                anchors.centerIn: parent

                onClicked: {
                    var companyInfo = {
                        "userID": appUser.user_id,
                        "name": companyFoundScreen.companyName,
                        "code": companyFoundScreen.countryCode,
                    }
                    companyInfo = settings.storage_get("companies_creation", companyInfo)

                    companyLoader.setSource(companyStack.createScreen, {"companyName": companyFoundScreen.companyName, "countryCode": companyFoundScreen.countryCode, "companies": companyFoundScreen.companies, "companyInfo": companyInfo})
                }
            }
        }
    }

    Desktop.BackArea {
        backArea.onClicked: {
            companyLoader.setSource(companyStack.searchScreen, {"companyNameDefault": companyFoundScreen.companyName, "countryCodeDefault": companyFoundScreen.countryCode})
        }
    }

    Connections {
        target: app.company_module

        onGetCompanyForMergeSuccess: {
            var mergeScreenCode = companyInfo.companyData && companyInfo.companyData.country_code ? companyInfo.companyData.country_code : ""
            var mergeScreenLegalCode = companyInfo.companyData && companyInfo.companyData.legal_address && companyInfo.companyData.legal_address.country ? companyInfo.companyData.legal_address.country : ""

            companyInfo["phoneNumbers"] = util.get_phone_numbers(application.countries.countries, companyInfo.companyData.phone_numbers, [companyFoundScreen.countryCode, mergeScreenCode, mergeScreenLegalCode])
            companyLoader.setSource(companyStack.mergeScreen, {"companies": companies, "companyName": companyFoundScreen.companyName, "countryCode": companyFoundScreen.countryCode, "companyInfo": companyInfo})
        }
    }
}
