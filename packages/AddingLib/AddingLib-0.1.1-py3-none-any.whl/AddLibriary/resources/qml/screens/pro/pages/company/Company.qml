import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Rectangle {
    id: companyStack

    color: ui.colors.dark3

    property var startScreen: "qrc:/resources/qml/screens/pro/pages/company/StartScreen.qml"
    property var searchScreen: "qrc:/resources/qml/screens/pro/pages/company/SearchScreen.qml"
    property var createScreen: "qrc:/resources/qml/screens/pro/pages/company/CreateScreen.qml"
    property var foundScreen: "qrc:/resources/qml/screens/pro/pages/company/FoundScreen.qml"
    property var createdScreen: "qrc:/resources/qml/screens/pro/pages/company/CreatedScreen.qml"
    property var mergeScreen: "qrc:/resources/qml/screens/pro/pages/company/MergeScreen.qml"
    property var waitScreen: "qrc:/resources/qml/screens/pro/pages/company/WaitScreen.qml"

    Component.onCompleted: {
        var screen = appUser.waiting_companies.length ? companyStack.waitScreen : companyStack.startScreen
        companyLoader.setSource(screen)
    }

    property var resendCodeTime: 120000
    property var confirmedEmails: {
        return {}
    }
    property var sendCodesTime: {
        return {}
    }
    property var sendCodesInfo: {
        return {}
    }

    signal makeCreateCompanyRequest()

    function timeDiff(information) {
        var nextTime = companyStack.sendCodesTime[information]
        if (!nextTime) return 0

        var currentTime = new Date()
        currentTime = currentTime.getTime()

        var result = nextTime - currentTime
        return result > 0 ? result : 0
    }

    property var linkLocale: {
        var locale = app.get_locale()
        var locales = ["en", "ru", "uk", "es", "de", "it", "fr"]

        if (locale == "ua") {
            locale = "uk"
        }
        if (!locales.includes(locale)) {
            locale = "en"
        }
        return locale
    }

    Loader {
        id: companyLoader

        anchors.fill: parent
    }

    Custom.BlockLoading {
        id: companyBlockLoading

        radius: 48
        minTime: 500

        startSignals: [
            app.company_module.searchCompanies,
            app.company_module.getCompanyForMerge,
        ]

        stopSignals: [
            app.company_module.searchCompaniesFailed,
            app.company_module.searchCompaniesFound,
            app.company_module.searchCompaniesNotFound,

            app.company_module.getCompanyForMergeSuccess,
            app.company_module.getCompanyForMergeFailed,
        ]
    }

    Connections {
        target: app.company_module

        onRequestCompanyEmailAccessConfirmationSuccess: {
            var date = new Date()
            companyStack.sendCodesTime[confirmationInfo.cluster_company_id] = date.getTime() + companyStack.resendCodeTime
            companyStack.sendCodesInfo[confirmationInfo.cluster_company_id] = confirmationInfo

            Popups.confirm_email_popup(confirmationInfo, companyStack, true)
        }

        onRequestNewEmailConfirmationSuccess: {
            var date = new Date()
            companyStack.sendCodesTime[confirmationInfo.email] = date.getTime() + companyStack.resendCodeTime
            companyStack.sendCodesInfo[confirmationInfo.email] = confirmationInfo

            Popups.confirm_email_popup(confirmationInfo, companyStack, false)
        }

        onConfirmCompanyEmailAccessSuccess: {
            companyStack.confirmedEmails[confirmationInfo.cluster_company_id.toLowerCase()] = confirmationInfo.email_token

            app.company_module.get_company_for_merge(confirmationInfo)
        }

        onConfirmNewEmailSuccess: {
            companyStack.confirmedEmails[confirmationInfo.email.toLowerCase()] = confirmationInfo.email_token

            companyStack.makeCreateCompanyRequest()
        }

        onCreateCompanySuccess: {
            companyLoader.setSource(companyStack.createdScreen, {"companyInfo": companyInfo})

            var deleteData = {
                "userID": appUser.user_id,
                "name": companyInfo["short_name"],
                "code": companyInfo["country_code"],
            }
            settings.storage_delete("companies_creation", deleteData)
        }

        onMergeCompaniesSuccess: {
            companyLoader.setSource(companyStack.waitScreen, {"companyInfo": companyInfo})
        }
    }
}
